let url = $(location).attr("href");

const regex = "dp\/.*\/";
const product_id = url.match(regex)[0].split("\/")[1];

$.get( "http://amazon.com/product-reviews/".concat(product_id), function( data ) {
    console.log(data);     
});


// $('div[data-hook=review-collapsed]').each(function(i, obj) {
//   console.log($( this ).text());
// });