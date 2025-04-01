$(document).ready(function() {
  // Event handler for go button in nav bar
  checkQueryString();

  // Interaction 1: DOM traversal. Fades the comment-box (parent) in AlternativeChickenCurry.html when the comment bar or button is clicked
  $('form#comment-bottom').on("click", function(event) {
    $(this).parent().fadeTo(500, 0.5);
    var logInMessage = $('<p class="log-in-message">You must log in to leave comments</p>');
    $(logInMessage).appendTo($(this).parent().parent()).fadeOut(500, function(){
      $(this).remove();
    });
  });
  // Stops the button from refreshing the page
  $('input#locked').on("click", function(event) {
    event.preventDefault();
  });

  // Interaction 2: Event Delegation.
  // Adds a pop up alert describing what the protein in the side bar is in list.html
  $("ul#side-tab a").on("mouseover", function(event) {
    let message = "";
    if ($(this).text() === 'Vegetarian' || $(this).text() === 'Gluten Free' || $(this).text() === 'Nut Free') {
      message = "This features recipes that are " + $(this).text() + " friendly.";
    } else {
      message = "This features recipes using " + $(this).text() + " as the primary protein source.";
    }
    $("#alert").text(message).show();
  }).on("mouseleave", function(event) {
    $("#alert").hide();
  });

  // Adds a highlight when hovering over a row in the grid in list.html
  $("table#table").on("mouseover", "tbody tr", function(event){
    $(this).css("background-color", "lightblue"); // Highlight the row
  }).on("mouseleave", "tbody tr", function(event) {
    $(this).css("background-color", ""); // Remove the highlight
  });

  adminDeletePopUp();
});

// function for the search bar requirement 
function checkQueryString(){
  var queryString = window.location.search;
  var urlParams = new URLSearchParams(queryString);
  if (urlParams.has('search-bar')){
    var keyword = urlParams.get('search-bar');
    if(keyword == 'Chicken' || keyword == 'chicken'){
      var ChickenHeading = $('<h3 class="search-result">Chicken</h3>');
      var ChickenColectionLink = $('<a class="chickenLink" href="list.html">Chicken Collection</a>');
      var ChickenRecipe1 = $('<a class="chickenLink" href="chickenCurry.html">Chicken Curry Recipe</a>');
      var ChickenRecipe2 = $('<a class="chickenLink" href="#">Chicken Pad Thai Recipe</a>');
      var ChickenRecipe3 = $('<a class="chickenLink" href="#">Chicken Pad See Ew Recipe</a>');
      var ChickenRecipe4 = $('<a class="chickenLink" href="#">Chicken Tortas Recipe</a>');
      var ChickenRecipe5 = $('<a class="chickenLink" href="#">Chicken Dip Recipe</a>');
      var ChickenRecipe6 = $('<a class="chickenLink" href="#">Chicken Alfredo Recipe</a>');
      $('#content').append(ChickenHeading);
      $('#content').append(ChickenColectionLink);
      $('#content').append(ChickenRecipe1);
      $('#content').append(ChickenRecipe2);
      $('#content').append(ChickenRecipe3);
      $('#content').append(ChickenRecipe4);
      $('#content').append(ChickenRecipe5);
      $('#content').append(ChickenRecipe6);
    } else {
      window.alert("There are no search results. Please search Chicken or chicken");
    }
  }
}

// Project 4: presents a pop-up for deleting a recipe from the listview
function adminDeletePopUp() {
  $('table#table tbody tr td form button').on("click", function(event) {
    event.preventDefault();
    confirm("Do you wish to delete this entry?");
  });
}