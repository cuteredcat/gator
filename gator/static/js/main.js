var pageAutoSearch;

var autoUpdate = function() {
  $.ajax({
    url: window.location.href,
    success: function(data) {
      var articleHeight = $(".page article:first-child").outerHeight(true);
      $(".page").css("height", articleHeight * data["news"].length + "px");

      showNews(data["news"], true);
      $(".page article:not(.updated)").remove();

      for (var i = 0; i < data["news"].length; i++) {
        $("#" + data["news"][i]["_id"]["$oid"]).css("top", (articleHeight * i) + "px");
      }
    }
  });
}

var autoSearch = function() {
  // remove all news
  $(".page article").remove();

  $.ajax({
    url: window.location.href.split("?")[0],
    data: { search: $("#search").val() },
    success: function(data) {
      showNews(data["news"], true);
    }
  });
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
             .attr("src", pageImagesUrl + "media/" + row["media"] + ".png");

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
    if (pageStamp > 0) {
      console.log("New valid stamp: " + pageStamp);
      var updateInterval = setInterval(function() {
        console.log("Update now!");

        $.ajax({
          url: "/timeline/" + (updateStamp || pageStamp) + "/",
          data: { search: $("#search").val() },
          success: function(data) {
            showNews(data["news"].reverse(), false);
            updateStamp = parseInt(data["stamp"]);
          }
        });
      }, 60000);
    }

    // autosearch after input value
    $("#search").on("keyup", function(event) {
      clearTimeout(pageAutoSearch);
      pageAutoSearch = setTimeout(autoSearch, 500);
    });
  }
  else if ($(".page.last").length) {
    console.log("Auto update with rating!");
    var updateInterval = setInterval(autoUpdate, 20000);
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

var pageLoading = false;

$(window).scroll(function() {
  if($(".page.timeline").length && !pageLoading && $(document).height() - ($(window).scrollTop() + $(window).height()) < 300) {
    // load next page
    console.log("Next page!");

    // show loader
    $("#loader").show();
    pageLoading = true;
    pageNumber += 1;

    $.ajax({
      url: "/timeline/" + (updateStamp || pageStamp) + "/",
      data: { page: pageNumber, search: $("#search").val() },
      success: function(data) {
        showNews(data["news"], true);
        pageLoading = false;
      },
      complete: function() {
        // hide loader
        $("#loader").hide();
      }
    });
  }
});
