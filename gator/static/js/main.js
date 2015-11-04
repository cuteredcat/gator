var showNews = function(newslist, append) {
  for (var i = 0, len = newslist.length; i < len; i++) {
    var row = newslist[i];

    if (!$("#" + row["_id"]["$oid"]).length) {
      var article = $("<article><a><span></span><img /></a></article>"),
          date = new Date(row["created_at"]["$date"]),
          hours = "0" + date.getHours(),
          minutes = "0" + date.getMinutes();

      article.attr("id", row["_id"]["$oid"]);

      if (!append) {
        article.css("height", 0)
               .animate({"height": "20px"}, 500)
               .addClass("last");
      }

      article.find("a")
             .addClass(row["tags"].join(" "))
             .attr("href", row["link"])
             .attr("target", "_blank")
             .append(row["text"]);

      article.find("a").attr("title", article.find("a")[0].hostname);

      article.find("span")
             .append(hours.substr(-2) + ":" + minutes.substr(-2));

      article.find("a > img")
             .attr("src", page_images_url + "media/" + row["media"] + ".png");

      if (append) { $("section.page.index").append(article); }
      else { $("section.page.index").prepend(article); }
    }
  }
}

$(document).ready(function() {
  // update page content each minute or so
  if (page_timestamp > 0) {
    console.log("New valid timestamp: " + page_timestamp);
    var updateInterval = setInterval(function() {
      console.log("Update now!");

      $.ajax({
        url: "/" + (update_timestamp || page_timestamp) + "/",
        success: function(data) {
          showNews(data["newslist"].reverse(), false);
          update_timestamp = parseInt(data["timestamp"]);
        }
      });
    }, 60000);
  }

  // init copy to clipboard button
  $(".page").on("click", ".copy-to-clipboard", function(event) {
    $('#' + $(event.target).data('copy-target')).select();

    try {
      var successful = document.execCommand('copy');
      var msg = successful ? 'successful' : 'unsuccessful';
      if (console) { console.log('Copying text command was ' + msg); }
    } catch(err) {
      if (console) { console.log('Oops, unable to cut'); }
    }

    // don't submit the form
    event.preventDefault();
  });
});

$(document).mousemove(function() {
  // remove class last from news
  $("article.last").removeClass("last");
});

var page_loading = false;

$(window).scroll(function() {
  if(!page_loading && $(document).height() - ($(window).scrollTop() + $(window).height()) < 300) {
    // load next page
    console.log("Next page!");

    // show loader
    $("#loader").show();
    page_loading = true;
    page_number += 1;

    $.ajax({
      url: "/" + page_timestamp + "/page/" + page_number + "/",
      success: function(data) {
        showNews(data["newslist"], true);
        page_loading = false;
      },
      complete: function() {
        // hide loader
        $("#loader").hide();
      }
    });
  }
});
