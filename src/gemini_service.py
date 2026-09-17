import os
import random
import time
import logging
import httpx

from dotenv import load_dotenv
from google import genai
from google.genai import errors
from google.genai import types


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# LOGGING CONFIGURATION
# ============================================================

LOG_LEVEL = os.getenv(
    "GEMINI_LOG_LEVEL",
    "INFO"
).upper()

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    ),
)

logger = logging.getLogger("nafulearn.gemini")


# ============================================================
# API KEY
# ============================================================

api_key = os.getenv("Gemini_api_key")

if not api_key:
    raise ValueError(
        "Gemini_api_key not found in .env file"
    )


# ============================================================
# MODEL CONFIGURATION
# ============================================================

PRIMARY_MODEL = os.getenv(
    "GEMINI_PRIMARY_MODEL",
    "gemini-3.6-flash"
)

FALLBACK_MODEL = os.getenv(
    "GEMINI_FALLBACK_MODEL",
    "gemini-3.5-flash-lite"
)


# ============================================================
# RETRY AND TIMEOUT CONFIGURATION
# ============================================================

MAX_RETRIES = int(
    os.getenv(
        "GEMINI_MAX_RETRIES",
        "3"
    )
)

INITIAL_DELAY = float(
    os.getenv(
        "GEMINI_INITIAL_DELAY",
        "2"
    )
)

MAX_DELAY = float(
    os.getenv(
        "GEMINI_MAX_DELAY",
        "10"
    )
)

TIMEOUT = int(
    os.getenv(
        "GEMINI_TIMEOUT",
        "60000"
    )
)


# ============================================================
# GEMINI HTTP CONFIGURATION
# ============================================================

http_options = types.HttpOptions(
    timeout=TIMEOUT,
    retry_options=types.HttpRetryOptions(
        attempts=1
    )
)


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=api_key,
    http_options=http_options
)


# ============================================================
# TRANSIENT ERROR CHECK
# ============================================================

def is_retryable_error(error):
    """
    Determine whether an error is temporary
    and therefore worth retrying.

    Retryable Gemini API errors:

        408 - Request timeout
        429 - Rate limit / quota pressure
        500 - Internal server error
        502 - Bad gateway
        503 - Service unavailable
        504 - Gateway timeout

    Retryable network errors:

        httpx.TimeoutException
        httpx.NetworkError
        httpx.RemoteProtocolError
    """

    # --------------------------------------------------------
    # GEMINI API ERRORS
    # --------------------------------------------------------

    if isinstance(error, errors.APIError):

        retryable_status_codes = {
            408,
            429,
            500,
            502,
            503,
            504,
        }

        return error.code in retryable_status_codes

    # --------------------------------------------------------
    # HTTP / NETWORK ERRORS
    # --------------------------------------------------------

    if isinstance(
        error,
        (
            httpx.TimeoutException,
            httpx.NetworkError,
            httpx.RemoteProtocolError,
        ),
    ):
        return True

    return False


# ============================================================
# WAIT BEFORE RETRY
# ============================================================

def wait_before_retry(attempt):
    """
    Wait using exponential backoff with jitter.

    Approximate delays:

        attempt 0 -> 2 seconds
        attempt 1 -> 4 seconds
        attempt 2 -> 8 seconds
    """

    exponential_delay = INITIAL_DELAY * (2 ** attempt)

    delay = min(
        exponential_delay,
        MAX_DELAY
    )

    jitter = random.uniform(
        0,
        1
    )

    total_delay = delay + jitter

    logger.warning(
        "Retrying Gemini request in %.1f seconds...",
        total_delay
    )

    time.sleep(total_delay)


# ============================================================
# GENERATE CONTENT
# ============================================================

def generate_content(
    prompt,
    primary_model=PRIMARY_MODEL,
    fallback_model=FALLBACK_MODEL,
    max_retries=MAX_RETRIES,
):
    """
    Generate content using Gemini.

    Strategy:

    1. Try the primary model.
    2. Retry temporary failures using exponential
       backoff with jitter.
    3. If the primary model cannot complete the request,
       try the fallback model.
    4. Do not retry permanent API errors.
    5. Return a safe user-facing message if all
       generation attempts fail.
    """

    # ========================================================
    # PRIMARY MODEL
    # ========================================================

    for attempt in range(max_retries):

        try:

            logger.info(
                "Sending request to Gemini primary model: %s",
                primary_model
            )

            response = client.models.generate_content(
                model=primary_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=4000,
                    temperature=0.2,
                ),
            )

            if not response.text:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            logger.info(
                "Gemini primary model responded successfully: %s",
                primary_model
            )

            return response.text

        except Exception as error:

            logger.error(
                "Gemini error on primary model "
                "(attempt %d/%d) | type=%s | message=%s",
                attempt + 1,
                max_retries,
                type(error).__name__,
                str(error)
            )

            # ------------------------------------------------
            # PERMANENT ERROR
            # ------------------------------------------------

            if not is_retryable_error(error):

                logger.error(
                    "Gemini error is not retryable. "
                    "Moving to fallback model."
                )

                break

            # ------------------------------------------------
            # RETRY TEMPORARY ERROR
            # ------------------------------------------------

            if attempt < max_retries - 1:

                wait_before_retry(attempt)

            else:

                logger.error(
                    "Maximum retry attempts reached "
                    "for primary model '%s'.",
                    primary_model
                )

    # ========================================================
    # FALLBACK MODEL
    # ========================================================

    logger.warning(
        "Primary model '%s' could not complete the request. "
        "Activating fallback model '%s'.",
        primary_model,
        fallback_model
    )

    try:

        logger.info(
            "Sending request to Gemini fallback model: %s",
            fallback_model
        )

        response = client.models.generate_content(
            model=fallback_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                max_output_tokens=4000,
                temperature=0.2,
            ),
        )

        if not response.text:
            raise RuntimeError(
                "Fallback model returned an empty response."
            )

        logger.info(
            "Gemini fallback model responded successfully: %s",
            fallback_model
        )

        return response.text

    except errors.APIError as error:

        logger.error(
            "Fallback Gemini API error | status=%s | message=%s",
            error.code,
            error.message
        )

    except Exception as error:

        logger.exception(
            "Unexpected fallback Gemini error: %s",
            error
        )

    # ========================================================
    # FINAL USER-SAFE RESPONSE
    # ========================================================

    logger.error(
        "All Gemini generation attempts failed."
    )

    return (
        "I'm having trouble connecting to my "
        "learning service right now. "
        "Please try again in a moment."
    )


# ============================================================
# STREAM CONTENT
# ============================================================

def stream_content(
    prompt,
    primary_model=PRIMARY_MODEL,
    fallback_model=FALLBACK_MODEL,
):
    """
    Stream Gemini's response as it is generated.

    Unlike generate_content(), this function does not wait
    for Gemini to finish the entire response.

    Each piece of generated text is yielded immediately
    so that the Flask application can send it to the browser.

    Strategy:

    1. Try the primary model.
    2. Stream its response chunk by chunk.
    3. If the primary model fails, use the fallback model.
    4. If both fail, send a safe user-facing message.
    """

    # ========================================================
    # PRIMARY MODEL
    # ========================================================

    try:

        logger.info(
            "Starting streaming request to Gemini primary model: %s",
            primary_model
        )

        response_stream = (
            client.models.generate_content_stream(
                model=primary_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=4000,
                    temperature=0.2,
                ),
            )
        )

        received_content = False

        for chunk in response_stream:

            if chunk.text:

                received_content = True

                logger.debug(
                    "Received Gemini streaming chunk "
                    "from primary model."
                )

                yield chunk.text

        if received_content:

            logger.info(
                "Gemini primary streaming completed successfully: %s",
                primary_model
            )

            return

        raise RuntimeError(
            "Gemini primary model returned an empty stream."
        )

    except Exception as error:

        logger.error(
            "Gemini streaming error on primary model | "
            "type=%s | message=%s",
            type(error).__name__,
            str(error)
        )


    # ========================================================
    # FALLBACK MODEL
    # ========================================================

    logger.warning(
        "Primary streaming model '%s' failed. "
        "Activating fallback model '%s'.",
        primary_model,
        fallback_model
    )

    try:

        logger.info(
            "Starting streaming request to Gemini fallback model: %s",
            fallback_model
        )

        response_stream = (
            client.models.generate_content_stream(
                model=fallback_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=4000,
                    temperature=0.2,
                ),
            )
        )

        received_content = False

        for chunk in response_stream:

            if chunk.text:

                received_content = True

                logger.debug(
                    "Received Gemini streaming chunk "
                    "from fallback model."
                )

                yield chunk.text

        if received_content:

            logger.info(
                "Gemini fallback streaming completed successfully: %s",
                fallback_model
            )

            return

        raise RuntimeError(
            "Gemini fallback model returned an empty stream."
        )

    except Exception as error:

        logger.exception(
            "Fallback Gemini streaming error: %s",
            error
        )


    # ========================================================
    # FINAL USER-SAFE RESPONSE
    # ========================================================

    logger.error(
        "All Gemini streaming attempts failed."
    )

    yield (
        "I'm having trouble connecting to my "
        "learning service right now. "
        "Please try again in a moment."
    )


# ============================================================
# HEALTH CHECK
# ============================================================

def health_check():
    """
    Check whether the configured primary Gemini model
    is reachable and available.

    Returns:
        True  -> Gemini service is healthy
        False -> Gemini service is unavailable
    """

    logger.info(
        "Running Gemini health check for model: %s",
        PRIMARY_MODEL
    )

    try:

        model = client.models.get(
            model=PRIMARY_MODEL
        )

        logger.info(
            "Gemini health check passed | model=%s",
            model.name
        )

        return True

    except Exception as error:

        logger.error(
            "Gemini health check failed | type=%s | message=%s",
            type(error).__name__,
            str(error)
        )

        return False


# ============================================================
# TEST THE SERVICE
# ============================================================

if __name__ == "__main__":

    logger.info("=" * 70)
    logger.info("NAFULEARN — GEMINI SERVICE TEST")
    logger.info("=" * 70)

    logger.info(
        "Primary model: %s",
        PRIMARY_MODEL
    )

    logger.info(
        "Fallback model: %s",
        FALLBACK_MODEL
    )

    logger.info(
        "Maximum retries: %d",
        MAX_RETRIES
    )

    healthy = health_check()

    print("\n" + "-" * 70)
    print("GEMINI HEALTH")
    print("-" * 70)

    print(
        "HEALTHY" if healthy else "UNHEALTHY"
    )

    test_prompt = """
    Explain what an abacus is to a Grade 10
    Computer Studies student in Kenya.
    """

    answer = generate_content(
        test_prompt
    )

    print("\n" + "-" * 70)
    print("GEMINI RESPONSE")
    print("-" * 70)

    print(answer)

    print("\n" + "=" * 70)