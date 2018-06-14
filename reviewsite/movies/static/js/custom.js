function get_movies() {
    $.ajax({
    url: "/movies/movies-cl/",
    type: 'GET',
    dataType: 'json',
    success: function(res) {
            update_movies(res);
        }
    });
}


function get_movie_by_id(id) {
    // alert(id);
    $.ajax({
    url: "/movies/movies-rud/"+ id,
    type: 'GET',
    dataType: 'json',
    success: function(res) {
        // array of reviews
        var reviews = res.reviews;

        // about movie
        var str = res.image;
        var image = str.match("(.static.*)")[0];
        var title = res.title;
        var trailer = res.trailer;
        var movie_rating = res.movie_rating;
        var release_date = res.release_date;
        var synopsis = res.synopsis;

        var trailer_html = "<a href=\'"+ trailer +"' class=\"text-white\" target='_blank'>\n" +
            "              " + title + "\n" +
            "            </a>";
        var tailer_id = $("#movie-trailer");
        tailer_id.html(trailer_html);

        var movie_rating_id = $("#movie-rating");
        movie_rating_id.html(movie_rating);

        var img = "<img class=\"img-responsive\" src=\'"+ image +"' height=\"200\"  width=\"400\" alt=\"Image "+ title +"\">"
        var img_id = $("#movie-img");
        img_id.html(img);

        var movie_title = $("#movie-title");
        var movie_title_html = "<h3>"+ title +"</h3>"
        movie_title.html(movie_title_html);

        var rel_id = $("#movie-rel");
        rel_id.html(release_date);

        var movie_summary = $("#movie-summary");
        movie_summary.html(synopsis);

        update_comments(reviews);
        }
    });
}

function update_comments(reviews) {
    var comment_html = "";
    var len = reviews.length;
    var reviews_comment = $("#reviews_comment");

    for(x=0; x<len; x++){

        var comment = "<div class=\"media text-muted pt-3\">\n" +
    "          <img data-src=\"holder.js/32x32?theme=thumb&bg=007bff&fg=007bff&size=1\" alt=\"\" class=\"mr-2 rounded\">\n" +
    "          <p class=\"media-body pb-3 mb-0 small lh-125 border-bottom border-gray\">\n" +
    "            <strong class=\"d-block text-gray-dark\">" + reviews[x].review_title + "</strong>\n" +
    "            <strong class=\"d-block text-gray-dark\"> Rating:" + reviews[x].rating + "</strong>\n" +
    "            "+ reviews[x].review +"" +
    "          </p>\n" +
    "        </div>";
        comment_html = comment_html + comment;
    }
    reviews_comment.html(comment_html);

}

// q = /movies/movies-cl/?q=2
function search_movie() {
    // alert("Inside search");
    var q = $("#movieSearch").val();
    $.ajax({
    url: "/movies/movies-cl/?q="+ q ,
    type: 'GET',
    dataType: 'json',
    success: function(res) {
            update_movies(res);
        }
    });

}

function update_movies(res) {
    var movies = res.length;
    var id = $("#bmovies");
    var divhtml = "";
    for(x=0; x<movies; x++){

        var pk = res[x].pk;
        var title = res[x].title;
        var release_date = res[x].release_date;
        var str = res[x].image;
        var image = str.match("(.static.*)");

        // alert(image);
        var row_data = "<div class=\"col-md-4 mx-auto\">\n" +
            "            <div class=\"card\" style=\"width: 18rem;\">\n" +
            "              <img class=\"card-img-top\" src='" + image[0] + "' alt=\"Card image cap\">\n" +
            "                <div class=\"card-body\">\n" +
            "                    <h5 class=\"card-title\">"+ title +"</h5>\n" +
            "                    <p class=\"card-text\">" + release_date + "</p>\n" +
            "                    <a href=\"/movies/about-movie/"+ pk +"\" class=\"btn btn-primary\">Read about movie</a>\n" +
            "                </div>\n" +
            "            </div>\n" +
            "          </div>";
        divhtml = divhtml + row_data;
    }
    id.html(divhtml);
}


function add_comment(id) {
    var object = new Object();
    object.title = $("#id_title").val();
    object.rating = $("#id_rating").val();
    object.review = $("#id_review").val();
    object.id = id;

    // alert(object);
    $.ajax({
    url: "/movies/post-review/",
    type: 'POST',
    dataType: 'json',
        data: object,
    success: function(res) {
            if(res.success === true){
                alert("Review saved!");
                window.location.href = "/movies/about-movie/" + id;
            }
        }
    });

}
