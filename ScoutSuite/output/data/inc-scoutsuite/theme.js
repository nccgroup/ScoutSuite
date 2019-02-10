const DARK_BOOTSTRAP_THEME = "inc-bootstrap/css/bootstrap-dark.min.css";
const LIGHT_BOOTSTRAP_THEME = "inc-bootstrap/css/bootstrap-light.min.css";

const DARK_SCOUT_THEME = "inc-scoutsuite/css/scoutsuite-dark.css";
const LIGHT_SCOUT_THEME = "inc-scoutsuite/css/scoutsuite-light.css";

$(document).ready(() => {
    if (localStorage.getItem("theme_checkbox") == "true") {
        document.getElementById("theme_checkbox").checked = true;
    }
});

function loadLastTheme() {
    if (localStorage.getItem("theme_checkbox") == "true") {
        setBootstrapTheme(DARK_BOOTSTRAP_THEME);
        setScoutTheme(DARK_SCOUT_THEME);
    }
}

/**
 * Toggles between light and dark themes
 */
function toggleTheme() {
    if (document.getElementById("theme_checkbox").checked) {
        this.setBootstrapTheme(DARK_BOOTSTRAP_THEME)
        this.setScoutTheme(DARK_SCOUT_THEME)
    }
    else {
        this.setBootstrapTheme(LIGHT_BOOTSTRAP_THEME)
        this.setScoutTheme(LIGHT_SCOUT_THEME)
    }
    localStorage.setItem("theme_checkbox", document.getElementById("theme_checkbox").checked);
};

/**
 * Toggles between light and dark themes
 */
function toggleTheme() {
    if (document.getElementById("theme_checkbox").checked) {
        this.setBootstrapTheme(DARK_BOOTSTRAP_THEME)
        this.setScoutTheme(DARK_SCOUT_THEME)
    }
    else {
        this.setBootstrapTheme(LIGHT_BOOTSTRAP_THEME)
        this.setScoutTheme(LIGHT_SCOUT_THEME)
    }
    localStorage.setItem("theme_checkbox", document.getElementById("theme_checkbox").checked);
};

/**
 * Sets the css file location received as the bootstrap theme
 * @param file
 */
function setBootstrapTheme(file) {
    document.getElementById("bootstrap-theme").href = file;
}

/**
 * Sets the css file location received as the scout theme
 * @param file
 */
function setScoutTheme(file) {
    document.getElementById("scout-theme").href = file;
}

