function searchAndScroll() {
    // Prevent the default form submission behavior
    event.preventDefault();

    // Get the search term from the input field
    var searchTerm = document.getElementById("searchInput").value.toLowerCase();

    // Get all elements with the class 'content'
    var contents = document.getElementsByClassName("content");

    console.log("Search term:", searchTerm); // Debugging statement

    // Loop through each content element
    for (var i = 0; i < contents.length; i++) {
        var content = contents[i].textContent.toLowerCase();

        console.log("Content:", content); // Debugging statement

        // If the content contains the search term, scroll to it and return false to prevent the form submission
        if (content.includes(searchTerm)) {
            contents[i].scrollIntoView();
            console.log("Keyword found at index:", i); // Debugging statement
            return false;
        }
    }

    // If search term not found, display an alert
    alert("Keyword not found");
    return false;
}