function scrape() {
    let url = $(location).attr("href");
    
    const regex = "dp\/.*[\/?]";
    const product_id = url.match(regex)[0].split("\/")[1];
    
    let reviews = [];
    
    for (i=1; i<11; i++) {
        $.get("https://www.amazon.com/product-reviews/".concat(product_id) + "/ref=cm_cr_arp_d_paging_btm_next_" + i.toString() + "?ie=UTF8&reviewerType=all_reviews&pageNumber=" + i.toString(), function( data ) {
            $(data).find('span[data-hook=review-body]').each(function(i, obj) {
                reviews.push($(this).text().trim());
            });
        });
    };
    
    return reviews;
};


console.log(scrape());
chrome.storage.local.get("api_key").then(function(data) {
    console.log(data['api_key'])
});