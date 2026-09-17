// ==========================================
// NafuLearn Global Theme System
// ==========================================


// ==========================================
// Apply Theme
// ==========================================

function applyTheme(theme) {

    const root =
        document.documentElement;


    // --------------------------------------
    // Light Mode
    // --------------------------------------

    if (theme === "light") {

        root.removeAttribute("data-theme");

        return;
    }


    // --------------------------------------
    // Dark Mode
    // --------------------------------------

    if (theme === "dark") {

        root.setAttribute(
            "data-theme",
            "dark"
        );

        return;
    }


    // --------------------------------------
    // System Default
    // --------------------------------------

    if (theme === "system") {

        const prefersDark =
            window.matchMedia(
                "(prefers-color-scheme: dark)"
            ).matches;


        if (prefersDark) {

            root.setAttribute(
                "data-theme",
                "dark"
            );

        } else {

            root.removeAttribute(
                "data-theme"
            );

        }
    }
}


// ==========================================
// Get Saved Theme
// ==========================================

function getSavedTheme() {

    return (
        localStorage.getItem(
            "nafulearn-theme"
        ) || "system"
    );
}


// ==========================================
// Initialize Theme
// ==========================================

function initializeTheme() {

    const savedTheme =
        getSavedTheme();

    applyTheme(savedTheme);
}


// ==========================================
// Save Theme
// ==========================================

function setTheme(theme) {

    localStorage.setItem(
        "nafulearn-theme",
        theme
    );

    applyTheme(theme);
}


// ==========================================
// Listen for System Theme Changes
// ==========================================

const systemTheme =
    window.matchMedia(
        "(prefers-color-scheme: dark)"
    );


systemTheme.addEventListener(
    "change",
    function () {

        const savedTheme =
            getSavedTheme();


        if (savedTheme === "system") {

            applyTheme("system");

        }

    }
);


// ==========================================
// Initialize Immediately
// ==========================================

initializeTheme();