// you can use app's unique identifier here
const LOCAL_STORAGE_KEY = "toggle-bootstrap-theme";
const LOCAL_META_DATA = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY));
// you can change this url as needed
const DARK_THEME_PATH = "https://cdnjs.cloudflare.com/ajax/libs/Halfmoon/1.1.1/css/halfmoon.min.css";
const DARK_STYLE_LINK = document.getElementById("dark-theme-style");
const THEME_TOGGLER = document.getElementById("theme-toggler");
let isDark = LOCAL_META_DATA && LOCAL_META_DATA.isDark;
// check if user has already selected dark theme earlier
if (isDark) {
  // enableDarkTheme();
  enableDarKModeByAddingClassFunction();
} else {
  // disableDarkTheme();
  disableDarKModeByAddingClassFunction();

}
/**
 * Apart from togglin// app's unique identifier here
  const LOCAL_STORAGE_KEY = "toggle-bootstrap-theme";
  const LOCAL_META_DATA = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY));
  // you can change this url as needed
  const DARK_THEME_PATH = "https://cdnjs.cloudflare.com/ajax/libs/Halfmoon/1.1.1/css/halfmoon.min.css";
  const DARK_STYLE_LINK = document.getElementById("dark-theme-style");
  const THEME_TOGGLER = document.getElementById("theme-toggler");
  let isDark = LOCAL_META_DATA && LOCAL_META_DATA.isDark;
  // check if user has already selected dark theme earlier
  if (isDark) {
    enableDarkTheme();
  } else {
    disableDarkTheme();
  }
  /**
   * Apart from toggling themes, this will also store user's theme preference in local storage.
   * So when user visits next time, we can load the same theme.
   *
   */
  function toggleTheme() {
    //enableDarKModeByAddingClassFunction():
    isDark = !isDark;
    if (isDark) {
      // enableDarkTheme();
      enableDarKModeByAddingClassFunction();
    } else {
      // disableDarkTheme();
      disableDarKModeByAddingClassFunction();

    }
    const META = { isDark };
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(META));
  }
  function toggleThemeTest() {
    enableDarKModeByAddingClassFunction();
  }

  function enableDarKModeByAddingClassFunction() {
    // Pulls id="myFooter"; removes light_mode_classes and flips tto dark_mode_classes
    // Remove .bg-ligt -> Add .bg-dark
    // Remove "text-primary" -> Add text-dark
    var element = document.getElementById("myFooter");
    element.classList.remove("bg-light");
    element.classList.add("bg-dark");
    element.classList.remove("text-dark");
    element.classList.add("text-light");


    THEME_TOGGLER.innerHTML = "🌙 Dark";
  }

  function disableModeByAddingClassFunction() {
    // Pulls id="myDIV"; removes light_mode_classes and flips tto dark_mode_classes
    // Add .bg-ligt -> Remove .bg-dark
    // Add "text-primary" -> Remove text-dark
    var element = document.getElementById("myFooter");
    element.classList.add("bg-light");
    element.classList.remove("bg-dark");
    element.classList.add("text-dark");
    element.classList.remove("text-light");

    THEME_TOGGLER.innerHTML = "🌞 Light";

  }

function enableDarkTheme() {
  DARK_STYLE_LINK.setAttribute("href", DARK_THEME_PATH);
  THEME_TOGGLER.innerHTML = "🌙 Dark";
}
function disableDarkTheme() {
  DARK_STYLE_LINK.setAttribute("href", "");
  THEME_TOGGLER.innerHTML = "🌞 Light";
}

