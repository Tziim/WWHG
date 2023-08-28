      const searchIcon = document.getElementById("search-icon");
const searchInput = document.getElementById("search-input");

// Check if the search bar should be initially expanded or not
const isExpanded = sessionStorage.getItem("searchBarExpanded") === "false";
if (isExpanded) {
    expandSearchBar();
}

searchIcon.addEventListener("click", () => {
    toggleSearchBarState();
});

// Function to toggle the search bar state
function toggleSearchBarState() {
    searchInput.classList.toggle("active");
    searchInput.focus();
    searchInput.value = ""; // Clear input when expanding
    toggleWidth();

    // Store the state in sessionStorage
    sessionStorage.setItem("searchBarExpanded", searchInput.classList.contains("active"));
}

// Toggle the width of the search container and input
function toggleWidth() {
    const width = searchInput.classList.contains("active") ? "250px" : "50px";
    searchInput.style.width = width;
    searchInput.style.padding = searchInput.classList.contains("active") ? "8px 12px" : "0";
    searchInput.style.opacity = searchInput.classList.contains("active") ? "1" : "0";
}

// Function to expand the search bar
function expandSearchBar() {
    searchInput.classList.add("active");
    toggleWidth();
}