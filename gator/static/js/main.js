var pageDelta, autoTimeout;

var autoUpdate = function() {
  if (pageDelta) { var url = "/lastnews-" + page_delta + ".json"; }
  else { var url = "/lastnews.json"; }

  $.ajax({
    url: url,
    success: function(data) {
      showNews(data["news"], true);

      $(".page article:not(.updated)").remove();

      var articleHeight = $(".page article:first-child").outerHeight(true);
      $(".page").css("height", articleHeight * data["news"].length + "px");

      for (var i = 0; i < data["news"].length; i++) {
        $("#" + data["news"][i]["_id"]["$oid"]).css("top", (articleHeight * i) + "px");
      }
    }
  });

  clearTimeout(autoTimeout);
  autoTimeout = setTimeout(autoUpdate, 20000);
}

var showNews = function(news, append) {
  // clear UPDATED class-flag
  $(".page article.updated").removeClass("updated");

  for (var i = 0, len = news.length; i < len; i++) {
    var row = news[i],
        shares = 0;

    // sum shares count
    for (var s = 0; s < row["shares"].length; s++) { shares += row["shares"][s]["count"]; }

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

      article.find("a > img")
             .attr("src", page_images_url + "media/" + row["media"] + ".png");

      if ($(".page.timeline").length) {
        article.find("span")
               .text(hours.substr(-2) + ":" + minutes.substr(-2));
      }
      else if ($(".page.last").length) {
        article.addClass("updated");
        article.data("shares", shares);

        article.find("span")
               .text(shares);
      }

      if (append) { $("section.page").append(article); }
      else { $("section.page").prepend(article); }
    }
    else {
      var article = $("#" + row["_id"]["$oid"]);

      if ($(".page.last").length) {
        article.addClass("updated");
        article.data("shares", shares);

        article.find("span")
               .text(shares);
      }
    }
  }
}

$(document).ready(function() {
  if ($(".page.timeline").length) {
    // update page content each minute or so
    if (page_stamp > 0) {
      console.log("New valid stamp: " + page_stamp);
      var updateInterval = setInterval(function() {
        console.log("Update now!");

        $.ajax({
          url: "/timeline/" + (update_stamp || page_stamp) + "/",
          success: function(data) {
            showNews(data["news"].reverse(), false);
            update_stamp = parseInt(data["stamp"]);
          }
        });
      }, 60000);
    }
  }
  else if ($(".page.last").length) {
    console.log("Auto update with rating!");

    // remap links
    $("a.lastnews").on("click", function(event) {
      pageDelta = $(this).data("delta");

      $(".page article").remove();
      autoUpdate();

      // don't open links
      event.preventDefault();
    });

    autoUpdate();
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
  if($(".page.timeline").length && !page_loading && $(document).height() - ($(window).scrollTop() + $(window).height()) < 300) {
    // load next page
    console.log("Next page!");

    // show loader
    $("#loader").show();
    page_loading = true;
    page_number += 1;

    $.ajax({
      url: "/timeline/" + page_stamp + "/page/" + page_number + "/",
      success: function(data) {
        showNews(data["news"], true);
        page_loading = false;
      },
      complete: function() {
        // hide loader
        $("#loader").hide();
      }
    });
  }
});
