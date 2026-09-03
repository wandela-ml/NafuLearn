# NafuLearn

### AI-Powered Learning for the Kenyan CBC Curriculum

> A practical AI/ML engineering project exploring how LLMs, embeddings, semantic retrieval, and Retrieval-Augmented Generation (RAG) can be used to create curriculum-grounded learning experiences.

**NafuLearn** is an AI-powered educational platform designed around Kenya's Competency-Based Curriculum (CBC).

The long-term vision is to support multiple CBC subjects and provide students with a more interactive learning experience. The current implementation focuses on **Grade 10 Computer Studies**, using curriculum content from the topic **Evolution of Computers — Early Computing Devices**.

### What I Built

* 📚 A structured curriculum knowledge base
* ✂️ A document chunking pipeline for lesson content
* 🧠 Semantic embeddings for curriculum sections
* 🔎 Semantic retrieval using cosine similarity
* 🤖 A Retrieval-Augmented Generation (RAG) pipeline
* 👩‍🏫 AI-generated lesson explanations
* ❓ AI-generated understanding questions
* 📝 AI-assisted student answer evaluation
* 🔄 Feedback and retry functionality
* 📖 Sequential lesson navigation through Learn Mode

### Technical Stack

`Python` · `Google Gemini` · `LLMs` · `Embeddings` · `RAG` · `Semantic Search` · `NumPy` · `Git` · `GitHub`

---

## Why NafuLearn?

Traditional digital learning platforms often present students with static curriculum content.

NafuLearn explores how modern AI techniques can create a more interactive learning experience where a student can:

1. Learn a curriculum topic.
2. Ask questions about the lesson.
3. Receive an explanation grounded in the available curriculum content.
4. Answer questions to test their understanding.
5. Receive AI-generated feedback.
6. Retry when their answer needs improvement.
7. Continue through the lesson sequentially.

The system is designed to prioritize **curriculum-grounded responses** rather than allowing the language model to freely generate unrelated information.


## Current Focus

The current knowledge base contains a Grade 10 Computer Studies lesson covering:

**Foundation → Evolution of Computers → Early Computing Devices**

Topics include:

* Early counting methods
* Abacus
* Napier's Bones
* Pascaline
* Slide Rule
* The evolution of early computing devices

The architecture is designed so that additional lessons and subjects can be added over time.

---

## System Architecture

The current NafuLearn architecture can be represented as:

**Curriculum Content → Chunking → Embeddings → Semantic Retrieval → RAG → Gemini LLM → Learning Interaction**

The learning interaction then follows:

**AI Explanation → Understanding Question → Student Answer → AI Evaluation → Feedback → Retry or Continue**

---

## RAG Pipeline

NafuLearn uses Retrieval-Augmented Generation to connect the language model to curriculum-specific content.

The pipeline works as follows:

**Knowledge Base**

↓

**Lesson Documents**

↓

**Text Chunking**

↓

**Gemini Embeddings**

↓

**Stored Embeddings**

↓

**Student Question**

↓

**Query Embedding**

↓

**Cosine Similarity**

↓

**Top-K Relevant Chunks**

↓

**Grounded Prompt**

↓

**Gemini**

↓

**Final Answer**

When a student asks a question, the system first searches the available curriculum content for the most semantically relevant sections. Those sections are then provided to the language model as context for generating the response.

This helps keep answers grounded in the available lesson content.

---

## Learn Mode

NafuLearn includes an interactive learning flow called **Learn Mode**.

The learning process is:

**Lesson Section**

↓

**AI Teaching Explanation**

↓

**Check Understanding Question**

↓

**Student Answer**

↓

**AI Evaluation**

↓

**Feedback**

↓

**Retry or Continue**

↓

**Next Lesson Section**

The system evaluates student responses using three classifications:

* **Correct**
* **Partially correct**
* **Needs improvement**

Students can retry an answer when their response needs improvement before continuing to the next section.

---

## Machine Learning and AI Components

### 1. Text Chunking

Curriculum lessons are divided into smaller structured chunks.

Chunking allows the retrieval system to search specific pieces of curriculum content instead of passing the entire lesson to the language model.

Each chunk contains content and metadata such as:

* Section
* Section order
* Content type
* Lesson information

---

### 2. Embeddings

Each lesson chunk is converted into a numerical vector representation using a Gemini embedding model.

These vectors represent the semantic meaning of the text and allow the system to compare a student's question with the stored curriculum content.

The current embedding implementation produces vectors with **3072 dimensions**.

---

### 3. Semantic Retrieval

When a student asks a question, NafuLearn:

1. Converts the question into an embedding.
2. Compares the query embedding with stored lesson embeddings.
3. Calculates cosine similarity.
4. Selects the most relevant chunks.
5. Passes the retrieved content to the language model.

This enables semantic search rather than relying only on exact keyword matches.

---

### 4. Retrieval-Augmented Generation

The retrieved curriculum sections are inserted into a grounded prompt.

The language model is instructed to:

* Use the provided lesson content as the primary source.
* Avoid inventing unsupported information.
* Explain concepts at a Grade 10 level.
* Clearly state when the current lesson does not contain enough information.

This creates a more controlled educational AI interaction.

---

## Example

### In-Context Question

**Question:**

> Who invented the Pascaline?

NafuLearn retrieves the relevant lesson content and generates a curriculum-grounded explanation identifying **Blaise Pascal** as the inventor of the Pascaline in **1642**.

### Out-of-Context Question

**Question:**

> What is quantum computing?

If the current lesson does not contain enough information to answer the question, NafuLearn is designed to acknowledge that limitation rather than presenting unrelated information as though it came from the curriculum.

This demonstrates an important aspect of grounded AI systems: **the assistant should recognize the limits of its available knowledge base.**

---

## Project Structure

The current project structure is:

NafuLearns/

├── data/

│   ├── embeddings/

│   │   └── lesson_01_embeddings.json

│   │

│   └── knowledge_base/

│       └── grade10/

│           └── computer_studies/

│               └── foundation/

│                   └── evolution_of_computers/

│                       └── lesson_01_early_computing.md

│

├── src/

│   ├── chunker.py

│   ├── embeddings.py

│   ├── learn_mode.py

│   ├── lesson_evaluator.py

│   ├── lesson_navigator.py

│   ├── lesson_teacher.py

│   ├── rag.py

│   └── retriever.py

│

├── .gitignore

├── README.md

└── .env

---

## Key Components

### `chunker.py`

Processes curriculum lesson content and divides it into structured chunks suitable for embedding and retrieval.

### `embeddings.py`

Generates vector embeddings for the lesson chunks.

### `retriever.py`

Handles semantic retrieval using:

* Query embeddings
* Cosine similarity
* Top-K retrieval

It also provides access to lesson sections and practice content.

### `rag.py`

Implements the Retrieval-Augmented Generation pipeline.

It:

1. Receives a student question.
2. Retrieves relevant curriculum chunks.
3. Builds a grounded prompt.
4. Sends the prompt to the language model.
5. Returns the generated answer.

### `lesson_teacher.py`

Generates explanations for individual lesson sections and creates a short understanding question.

### `lesson_evaluator.py`

Evaluates student responses against the provided lesson content and generates feedback.

### `lesson_navigator.py`

Controls movement through the lesson, including:

* Current section
* Next section
* Previous section
* Learning sections

### `learn_mode.py`

Combines teaching, evaluation, feedback, retry, and lesson navigation into an interactive learning experience.

---

## Technologies

### Programming

* Python

### Machine Learning and AI

* Google Gemini
* Embeddings
* Large Language Models (LLMs)
* Retrieval-Augmented Generation (RAG)
* Semantic Search
* Cosine Similarity

### Data Processing

* NumPy
* Markdown-based knowledge base

### Development

* Visual Studio Code
* Git
* GitHub
* Python virtual environments

---

## Engineering Concepts Demonstrated

This project demonstrates practical implementation of:

* Natural Language Processing
* Vector embeddings
* Semantic search
* Information retrieval
* Retrieval-Augmented Generation
* Prompt engineering
* LLM integration
* Grounded generation
* AI-based evaluation
* Modular Python application design
* Metadata-driven retrieval
* Error handling
* Environment-variable-based API configuration
* Git version control

---

## Future Roadmap

The long-term vision is to expand NafuLearn into a broader AI-powered CBC learning platform.

Planned improvements include:

* [ ] Expand the knowledge base to additional Grade 10 Computer Studies topics
* [ ] Add additional CBC subjects
* [ ] Add more lessons and curriculum levels
* [ ] Introduce a persistent vector database
* [ ] Improve retrieval ranking
* [ ] Add conversation history
* [ ] Add student progress tracking
* [ ] Build a web-based learning interface
* [ ] Add quizzes and assessments
* [ ] Add personalized learning paths
* [ ] Improve answer evaluation
* [ ] Add teacher and administrator functionality
* [ ] Deploy the complete platform

---

## Current Limitations

NafuLearn is currently a prototype under active development.

The current implementation:

* Uses a limited curriculum knowledge base.
* Focuses on Grade 10 Computer Studies.
* Uses locally stored embeddings.
* Does not yet use a production vector database.
* Does not yet have persistent student accounts.
* Does not yet track student progress.
* Does not yet represent the full Kenyan CBC curriculum.

These limitations represent areas for future development.

---

## Learning Goals

NafuLearn is a practical Machine Learning Engineering project designed to explore how different AI components can be combined into a complete educational application.

The project brings together:

**Data → Embeddings → Retrieval → LLM → Evaluation → User Interaction**

The goal is not simply to build another chatbot, but to explore how an LLM can be combined with structured curriculum knowledge, semantic retrieval, and learning interactions to create a more useful educational system.

---

## Author

**Marygoret Wandela**

Aspiring Machine Learning Engineer focused on:

* Python
* Machine Learning
* Natural Language Processing
* Computer Vision
* LLM Applications
* Retrieval-Augmented Generation

GitHub: https://github.com/wandela-ml

LinkedIn: https://www.linkedin.com/in/marygoret-wandela/

Email: [maryawandela@gmail.com](mailto:maryawandela@gmail.com)

---

## Project Philosophy

> Build practical AI systems that solve real problems.

NafuLearn explores how modern AI techniques can be applied to education in the Kenyan context, with the goal of making curriculum-based learning more interactive, accessible, and personalized.
