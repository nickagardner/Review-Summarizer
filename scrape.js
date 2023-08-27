async function scrape() {
    let url = $(location).attr("href");
    
    const regex = "dp\/.*[\/?]";
    const product_id = url.match(regex)[0].split("\/")[1];
    
    let reviews = [];

    for (i=1; i<11; i++) {
        $.get("https://www.amazon.com/product-reviews/".concat(product_id) + "/ref=cm_cr_arp_d_paging_btm_next_" + i.toString() + "?ie=UTF8&reviewerType=all_reviews&pageNumber=" + i.toString(), function( data ) {
            $(data).find('span[data-hook=review-body]').each(function(j, obj) {
                reviews.push($(this).text().trim());
            });
        });
    };

    chrome.storage.local.get("api_key").then(function(data) {
        reviews.push(data['api_key'])
    });

    await wait();
    
    return reviews;
};

function wait() {
    return new Promise(resolve => {
    setTimeout(resolve, 1000);
  });
}

async function postJSON() {
    var reviews = await scrape()
    try {
    const response = await fetch("https://review-summarizer-4e7213007e44.herokuapp.com/summarize", {
        method: "POST",
        body: JSON.stringify(reviews),
    });

    const result = await response.json();
    console.log("Success:", result);
  } catch (error) {
    console.error("Error:", error);
  }
}

postJSON();