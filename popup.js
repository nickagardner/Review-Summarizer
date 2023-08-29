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
    return [result["themes"], result["counts"]]
  } catch (error) {
    console.error("Error:", error);
  }
}

const button = document.querySelector("button");
button.addEventListener("click", async () => {
    const [themes, counts] = await postJSON();

    var count_ints = counts.map(function(str) {
        return parseInt(str); });
    var wrapped_themes = themes.map(function(str) {
        return str.replace(/(?![^\n]{1,15}$)([^\n]{1,15})\s/g, '$1<br>'); });

    var data = [
        {
          y: wrapped_themes.slice(0,5),
          x: count_ints.slice(0,5),
          type: 'bar',
          orientation: 'h',
          marker: {
            color: 'rgb(107, 255, 112)'
          },
          transforms: [{
            type: 'sort',
            target: 'x',
            order: 'ascending'
          }],
        }
      ];
    
    var layout = {
        title: 'What do reviewers like?',
        margin: {
            l: 100
        }
    };
    Plotly.newPlot('pos_themes', data, layout);

    var data = [
        {
          y: wrapped_themes.slice(5,10),
          x: count_ints.slice(5,10),
          type: 'bar',
          orientation: 'h',
          marker: {
            color: 'rgb(253, 96, 96)'
          },
          transforms: [{
            type: 'sort',
            target: 'x',
            order: 'ascending'
          }],
        }
      ];

    var layout = {
        title: 'What do reviewers dislike?',
        margin: {
            l: 100
        }
    };
    Plotly.newPlot('neg_themes', data, layout);
  });