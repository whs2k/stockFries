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


function toggleTheme() {
    //enableDarKModeByAddingClassFunction():
    isDark = !isDark;
    if (isDark) {
      // enableDarkTheme();
      enableDarKModeByAddingClassFunction();
      //enableDarKModeByAddingClassFunction_headNav();
    } else {
      // disableDarkTheme();
      disableModeByAddingClassFunction();
      //disableModeByAddingClassFunction_headNav();

    }
    const META = { isDark };
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(META));
  } 
function toggleThemeTest() {
  enableDarKModeByAddingClassFunction();
  }

// bodyDIV, headerNavDIV, footerDIV
function enableDarKModeByAddingClassFunction() {
   var element = document.getElementById("myDIV");
   element.classList.add("bg-dark");
   element.classList.remove("bg-light");
   element.classList.remove("text-dark");
   element.classList.add("text-light");
   var element = document.getElementById("headNavDIV");
   element.classList.add("bg-dark");
   element.classList.remove("bg-light");
   element.classList.remove("text-dark");
   element.classList.add("text-light");
   var element = document.getElementById("footerDIV");
   element.classList.add("bg-dark");
   element.classList.remove("bg-light");
   element.classList.remove("text-dark");
   element.classList.add("text-light");
   var element = document.getElementById("cardOneDIV");
   element.classList.add("bg-dark");
   element.classList.remove("bg-light");
   element.classList.remove("text-dark");
   element.classList.add("text-light");
   var element = document.getElementById("tableOneDIV");
   element.classList.add("table-dark");
   element.classList.remove("table-light");
   //element.classList.remove("text-dark");
   //element.classList.add("text-light");
   var element = document.getElementById("tableBodyOneDIV");
   element.classList.add("bg-dark");
   element.classList.remove("bg-light");
   element.classList.remove("text-dark");
   element.classList.add("text-light");
   

   //document.getElementById('logoHeaderImage').src="{{url_for('static', filename='logo_dark.png')}}";

   THEME_TOGGLER.innerHTML = "🌙 Dark"
}


function disableModeByAddingClassFunction() {
    // Pulls id="myDIV"; removes light_mode_classes and flips tto dark_mode_classes
    // Add .bg-ligt -> Remove .bg-dark
    // Add "text-primary" -> Remove text-dark
    var element = document.getElementById("myDIV");
    element.classList.add("bg-light");
    element.classList.remove("bg-dark");
    element.classList.add("text-dark");
    element.classList.remove("text-light");

    var element = document.getElementById("headNavDIV");
    element.classList.add("bg-light");
    element.classList.remove("bg-dark");
    element.classList.add("text-dark");
    element.classList.remove("text-light");
    var element = document.getElementById("footerDIV");
    element.classList.add("bg-light");
    element.classList.remove("bg-dark");
    element.classList.add("text-dark");
    element.classList.remove("text-light");
    var element = document.getElementById("cardOneDIV");
    element.classList.add("bg-light");
    element.classList.remove("bg-dark");
    element.classList.add("text-dark");
    element.classList.remove("text-light");
    var element = document.getElementById("tableOneDIV");
    element.classList.add("table-light");
    element.classList.remove("table-light");
    //element.classList.add("text-dark");
    //element.classList.remove("text-light");
    var element = document.getElementById("tableBodyOneDIV");
    element.classList.add("bg-light");
    element.classList.remove("bg-dark");
    element.classList.add("text-dark");
    element.classList.remove("text-light");
    

    //document.getElementById('logoHeaderImage').src="{{url_for('static', filename='logo.png')}}";

    THEME_TOGGLER.innerHTML = "🌞 Light";

  }


