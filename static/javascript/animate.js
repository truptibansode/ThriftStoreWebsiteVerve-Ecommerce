// Add an event listener to the window scroll event
window.addEventListener('scroll', function() {
    // Get all elements with the class 'latest-coll-sect'
    var latestCollSections = document.querySelectorAll('.latest-coll-sect');
    
    // Loop through each section
    latestCollSections.forEach(function(section) {
      // Get the position of the top of the section relative to the viewport
      var sectionTop = section.getBoundingClientRect().top;
    
      // Check if the section is in the viewport
      if (sectionTop < window.innerHeight) {
        // Add a CSS class to trigger the animation effect
        section.classList.add('animated');
      }
    });
  });
  