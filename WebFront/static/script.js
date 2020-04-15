// Get the hash of the url
const hash = window.location.hash
.substring(1)
.split('&')
.reduce(function (initial, item) {
  if (item) {
    var parts = item.split('=');
    initial[parts[0]] = decodeURIComponent(parts[1]);
  }
  return initial;
}, {});
window.location.hash = '';

// Set token
let _token = hash.access_token;

const authEndpoint = 'https://accounts.spotify.com/authorize';

// Replace with your app's client ID, redirect URI and desired scopes
const clientId = '0fe2926af3b44463b64fc2d34bed582c';
const redirectUri = 'https://propane-ground-269323.appspot.com';
//const redirectUri = 'http://localhost:8080';
const scopes = [
  'user-top-read'
];

var post_object;
// If there is no token, redirect to Spotify authorization
function auth() {
  if (!_token) {
    window.location = `${authEndpoint}?client_id=${clientId}&redirect_uri=${redirectUri}&scope=${scopes.join('%20')}&response_type=token&show_dialog=true`;
  }
}

num_songs = 50;
// Make a call using the token
$.ajax({
  url: "https://api.spotify.com/v1/me/top/tracks?limit=" + num_songs,
  type: "GET",
  beforeSend: function(xhr){xhr.setRequestHeader('Authorization', 'Bearer ' + _token );},
  success: function(data) {

    // remove the button
    $('#intro').remove();

    // save song data
    var songs = [];
    var songs_param = '';
    data.items.map(function(track) {
      songs.push({'id': track.id, 'name': track.name});
      songs_param += track.id + ','
    });

    songs_param = songs_param.slice(0,-1);

    $.ajax({
      url: "https://api.spotify.com/v1/audio-features/?ids=" + songs_param,
      type: "GET",
      beforeSend: function(xhr){xhr.setRequestHeader('Authorization', 'Bearer ' + _token );},
      success: function(tracks) {

        //var features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'liveness', 'valence', 'tempo']
        // put back to original order
        var features = ['danceability', 'energy', 'speechiness', 'acousticness', 'liveness', 'valence', 'loudness', 'tempo'];

        // compute averages
        tracks.audio_features.map(function(song) {
          for (var i in songs) {
            if (songs[i].id == song.id) {
              songs[i].danceability = song.danceability;
              songs[i].energy = song.energy;
              songs[i].speechiness = song.speechiness;
              songs[i].acousticness = song.acousticness;
              songs[i].liveness = song.liveness;
              songs[i].valence = song.valence;
              songs[i].loudness = song.loudness;
              songs[i].tempo = song.tempo;
            }
          }
        });

        var danceability_total = 0;
        var energy_total = 0;
        var speechiness_total = 0;
        var acousticness_total = 0;
        var liveness_total = 0;
        var valence_total = 0;
        var loudness_total = 0;
        var tempo_total = 0;

        for (i=0; i<songs.length; i++) {
          danceability_total += songs[i].danceability;
          energy_total += songs[i].energy;
          speechiness_total += songs[i].speechiness;
          acousticness_total += songs[i].acousticness;
          liveness_total += songs[i].liveness;
          valence_total += songs[i].valence;
          loudness_total += songs[i].loudness;
          tempo_total += songs[i].tempo;
        }

        var user_averages = {
          'how_offbeat': 0,
          'audio_features': {
            'danceability': danceability_total/num_songs,
            'energy': energy_total/num_songs,
            'speechiness': speechiness_total/num_songs,
            'acousticness': acousticness_total/num_songs,
            'liveness': liveness_total/num_songs,
            'valence': valence_total/num_songs,
            'loudness': loudness_total/num_songs,
            'tempo': tempo_total/num_songs
          }
        };

        post_object = {
          'how_offbeat': 0,
          "Values": {
            "danceability": danceability_total / num_songs,
            "energy": energy_total / num_songs,
            "loudness": loudness_total / num_songs,
            "speechiness": speechiness_total / num_songs,
            "acousticness": acousticness_total / num_songs,
            "liveness": liveness_total / num_songs,
            "valence": valence_total / num_songs,
            "tempo": tempo_total / num_songs
          }
        }

        var features_total = [
          danceability_total,
          energy_total,
          speechiness_total,
          acousticness_total,
          liveness_total,
          valence_total,
          loudness_total,
          tempo_total
        ];

        danceability_avg = Math.round(danceability_total / num_songs * 100);
        energy_avg = Math.round(energy_total / num_songs * 100);
        speechiness_avg = Math.round(speechiness_total / num_songs * 100);
        acousticness_avg = Math.round(acousticness_total / num_songs * 100);
        liveness_avg = Math.round(liveness_total / num_songs * 100);
        valence_avg = Math.round(valence_total / num_songs * 100);
        loudness_avg = Math.round(loudness_total / num_songs);
        tempo_avg = Math.round(tempo_total / num_songs);

        // profile section: structure & intro
        let structure_html = $('<div class="row" id="profile-row"><div class="col-md-4" id="profile-row-left"></div><div class="col-md-8" id="profile-row-right"></div></div>');
        structure_html.appendTo($('#content'));
        let average_text = $('<p style="margin-bottom:0px;">Your listening profile</p>');
        average_text.appendTo($('#profile-row-left'));
        let profile_description = $('<p style="font-size:12px; color:#ababab;">The average prevalence of 8 audio features <br>across your top 50 songs.</p>');
        profile_description.appendTo($('#profile-row-left'))

        // html for profile section
        let profile_section = $('<div id="profile_rect"></div>');
        profile_section.appendTo($('#profile-row-left'));

        // initial svg for profile section
        var profile_svg = d3.select('#profile_rect')
          .append('svg')
          .attr('height', 370)
          .attr('width', 360);

        // vertical lines
        profile_svg.append('line')
          .attr('stroke', '#d4d4d4')
          .attr('stroke-width', 1)
          .attr('x1', 130)
          .attr('x2', 130)
          .attr('y1', 0)
          .attr('y2', 361);

        // feature rects
        var rect_color = 'rgba(30, 215, 96, 0.5)';
        for (var i = 0; i < features_total.length - 2; i++) {
          // rect
          profile_svg.append('rect')
            .attr('fill', rect_color)
            .attr('height', 35)
            .attr('width', 200 * (features_total[i]/num_songs))
            .attr('x', 130)
            .attr('y', 7 + (i*45));
          // text
          profile_svg.append('text')
            .text(features[i])
            .attr('class','audio_feature')
            .attr('font-size', '14px')
            .attr('fill', '#717171')
            .attr('x', 123)
            .attr('text-anchor', 'end')
            .attr('y', 30 + (i*45))
          profile_svg.append('text')
            .text(Math.round(features_total[i]/num_songs * 100) + '%')
            .attr('font-size', '14px')
            .attr('fill', '#717171')
            .attr('x', 130 + (200 * (features_total[i]/num_songs) + 5))
            .attr('y', 30 + (i*45))
        };

        // loudness text
        profile_svg.append('text')
          .text('loudness') //+ Math.round(tempo_total/num_songs) + 'bpm')
          .attr('class', 'audio_feature')
          .attr('font-size', '14px')
          .attr('fill', '#717171')
          .attr('x', 123)
          .attr('text-anchor', 'end')
          .attr('y', 297);
        profile_svg.append('text')
          .text(Math.round(loudness_total / num_songs) + ' dB')
          .attr('font-size', '14px')
          .attr('fill', '#717171')
          .attr('x', 135)
          .attr('y', 297);

        // tempo text
        profile_svg.append('text')
          .text('tempo') //+ Math.round(tempo_total/num_songs) + 'bpm')
          .attr('class', 'audio_feature')
          .attr('font-size', '14px')
          .attr('fill', '#717171')
          .attr('x', 123)
          .attr('text-anchor', 'end')
          .attr('y', 342);
        profile_svg.append('text')
          .text(Math.round(tempo_total / num_songs) + 'bpm')
          .attr('font-size', '14px')
          .attr('fill', '#717171')
          .attr('x', 135)
          .attr('y', 342);

        // tooltips
        var tip = d3.tip()
          .attr('class', 'd3-tip')
          .offset([-10, 0])
          .html(function (d) {
              var text_hovered = d3.select(this).text();
              return text_hovered.startsWith('danceability') ? 'Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity.'
                   : text_hovered.startsWith('energy') ? 'Energy represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy.'
                   : text_hovered.startsWith('speechiness') ? 'Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the higher the value.'
                   : text_hovered.startsWith('acousticness') ? 'A confidence measure of whether the track is acoustic.'
                   : text_hovered.startsWith('liveness') ? 'Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live.'
                   : text_hovered.startsWith('valence') ? 'A measure describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).'
                   : text_hovered.startsWith('loudness') ? 'The overall loudness of a track in decibels (dB). Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typical range between -60 and 0 db.'
                   : text_hovered.startsWith('tempo') ? 'The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.'
                   : '';
          });
        profile_svg.call(tip);
        d3.selectAll('#profile_rect text.audio_feature')
          .on('mouseover', tip.show)
          .on('mouseout', tip.hide)

        // final question & button
        let offbeat_question = $('<p style="margin-bottom: 0px;">How offbeat do you want to get?</p>');
        let offbeat_question_subtext = $('<p style="font-size:12px; color:#ababab;">Choose the degree to which the recommendations will be different from the music you usually listen to (higher: more different, lower: less different).</p>');
        let slider = $('<div class="sliders"><div id="slider-offbeat"></div></div>');
        let explore_button = $('<button onclick="return_results()">Explore</button>');

        offbeat_question.appendTo($('#profile-row-left'));
        offbeat_question_subtext.appendTo($('#profile-row-left'));
        slider.appendTo($('#profile-row-left'));

        // slider
        var sliderOffbeat = d3
            .sliderBottom()
            .min(1).max(10)
            .step(1)
            .width(200)
            .default(10)
        var gTime = d3
            .select('div#slider-offbeat').append('svg')
            .attr('width', 250).attr('height', 70)
            .append('g')
            .attr('transform', 'translate(20,30)');
        gTime.call(sliderOffbeat);

        // final button to draw the svg
        explore_button.appendTo($('#profile-row-left'));

        // draw the legend
        let legend = $('<svg id="mylegend" width="700" height="60"></svg>');
        legend.appendTo($('#profile-row-right'));

        // draw the svg
        let circles = $('<svg id="mychart" width="700" height="700"></svg>');
        circles.appendTo($('#profile-row-right'));

      }
    });

  }
});

return_results = function () {

    // disable button
    $('button').prop("disabled", true);
    $('button').css("background-color", "#83cc9c");
    $('button').html(
      `<span class="spinner-border" style="width:3rem; height:3rem" role="status" aria-hidden="true"></span> Loading...`
    )

    var sliderVal = d3.select("#slider-offbeat").text().substring(11);
    post_object["how_offbeat"] = parseInt(sliderVal);

    $.ajax({
        url: './api/Path_to_Data',
        type: "POST",
        data: JSON.stringify(post_object),
        dataType: 'json',
        success: function (data) {
            var res_data = data
            drawGraph(res_data)
        }
    });
};

function drawGraph(res_data) {
    console.log(res_data)
  // clear the legend and all of the circle svg's child elements on redraw
  d3.select("#mylegend g").remove()
  d3.select("#mychart g").remove()
  d3.select(".d3-circle-tip").remove()

  // return button to correct state
  $('button').prop("disabled", false);
  $('button').css("background-color", "#1ed760");
  $('button').html(`Explore`)

  // draw the legend & text
  var cScale = d3.scaleSequential(d3.interpolateBlues)
    .domain([0,99]);

  var xScale = d3.scaleLinear()
      .domain([0,99])
      .range([0, 700]);

  var svg_legend = d3.select("#mylegend")
    .append("g")
  var legend_scale = d3.select("#mylegend")
    .selectAll("rect")
    .data(Array.from(Array(100).keys()))
    .enter().append("rect")
    .attr("x", (d) => Math.floor(xScale(d)))
    .attr("y", 0)
    .attr("width", (d) => {
      if (d == 99) {return 6;}
      else {return Math.floor(xScale(d+1)) - Math.floor(xScale(d)) + 1;}
    })
    .attr("height", 25)
    .attr("fill", (d) => cScale(d));

  svg_legend.append("text")
    .attr("x", 0)
    .attr("y", 38)
    .text("very close to")
    .style("font-size", "12px")
    .style("fill", "#ababab");
  svg_legend.append("text")
    .attr("x", 700)
    .attr("y", 38)
    .text("far away from")
    .style("font-size", "12px")
    .style("fill", "#ababab")
    .attr("text-anchor", "end");
  svg_legend.append("text")
    .attr("x", 0)
    .attr("y", 50)
    .text("your profile")
    .style("font-size", "12px")
    .style("fill", "#ababab");
  svg_legend.append("text")
    .attr("x", 700)
    .attr("y", 50)
    .text("your profile")
    .style("font-size", "12px")
    .style("fill", "#ababab")
    .attr("text-anchor", "end");

  // draw the graph
  var circles_svg = d3.select("#mychart"),
    margin = 20,
    diameter = + circles_svg.attr("width"),
    g = circles_svg.append("g")
      .attr("transform", "translate(" + diameter / 2 + "," + diameter / 2 + ")")
      .attr("id", "mychart-g");

  var color = d3.scaleLinear()
    .domain([-1, 5]) // for depths
    .range(["hsl(0,0%,97%)", "hsl(0,0%,50%)"]) // greys
    .interpolate(d3.interpolateHcl);

  var colorScale = d3.scaleSequential(d3.interpolateBlues) // for nodes at the very bottomn
    .domain([0,1])

  var pack = d3.pack()
    .size([diameter - margin, diameter - margin])
    .padding(2);

  //root = res_data

  root = d3.hierarchy(res_data)
    .sum(function(d) { return 1; })
    .sort(function(a, b) { return b.value - a.value; });

  var focus = root,
    nodes = pack(root).descendants(),
    view;

  var circle = g.selectAll("circle")
    .data(nodes)
    .enter().append("circle")
    .attr("class", function(d) { return d.parent ? d.children ? "node" : "node node--leaf" : "node node--root"; })
    .style("fill", function(d) {
      // console.log(d)
      return d.children ? color(d.depth-1) : colorScale(d.data.similarity);
    })
    .style("stroke", function(d) {
      return d.depth == 0 ? "rgba(30,215,96,1)" : ""
    })
    .style("stroke-width", function(d) {
      return d.depth == 0 ? 5 : 0
    })
    .on("click", function(d) {
      if (focus !== d) {
        if (d.height === 0) {song_tip.hide(d);};
        zoom(d), d3.event.stopPropagation();
      }
    })
    // control iframe visibility for songs on hover
    .on("mouseover", function(d){
      if (focus.height <= 2 & d.height === 0) {
        d3.select(".d3-circle-tip").transition().duration(100).style("opacity", "1");
        song_tip.show(d);
        var tooltip = d3.selectAll(".d3-circle-tip")
          .on('mouseover', function(d) {
            d3.select(".d3-circle-tip").transition().style("opacity", "1");
          })
          .on('mouseout', function(d) {
            d3.select(".d3-circle-tip").transition().duration(1000).style("opacity", "0").on("end", song_tip.hide);
          });
      }
    })
    .on("mouseout", function(d){
      if (focus.height <= 2 & d.height === 0) {
        d3.select(".d3-circle-tip").transition().duration(1000).style("opacity", "0").on("end", song_tip.hide);
      }
    });

  // tooltips for song iframes
  var song_tip = d3.tip()
    .attr('class', 'd3-circle-tip')
    .html(function(d) {
      var song_id = d.data.name;
      return '<iframe src="https://open.spotify.com/embed/track/' + song_id + '" width="300" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>';
    });
  circles_svg.call(song_tip);

  var text = g.selectAll("text")
  .data(nodes)
  .enter().append("text")
  .attr("class", "label")
  .style("fill-opacity", function(d) { return d.parent === root ? 1 : 0; })
  .style("display", function(d) { return d.parent === root ? "inline" : "none"; })
  text.append("tspan")
    .text(function(d) {
      if (d.height > 0 && d.depth > 0) {
        var obj = d.data.features;
        var first_key = Object.keys(obj)[0];
        var first_val = obj[first_key];
        var sign = (first_val >= 0) ? "+" : "-";
        return sign + first_key;
      } else {return "";}
    })
    .attr("x", 0)
    .attr("dx", 0)
    .attr("dy", -15)
    .attr("text-anchor", "middle");
  for (i=1; i<3; i++) {
    text.append("tspan")
      .text(function(d) {
        if (d.height > 0 && d.depth > 0) {
          var obj = d.data.features;
          var first_key = Object.keys(obj)[i];
          var first_val = obj[first_key];
          var sign = (first_val >= 0) ? "+" : "-";
          return sign + first_key;
        } else {return "";}
      })
      .attr("x", 0)
      .attr("dx", 0)
      .attr("dy", 15)
      .attr("text-anchor", "middle");
  }

  var node = g.selectAll("circle,text");

  // get a random circle
  var all_circles = d3.selectAll("circle");
  // zoom to the circle with songs that have the highest similarity
  var zoom_circles = Object.values(all_circles._groups[0]).filter(circle => circle.__data__.height === 1); // level 1 starting zoom
  var highest_similarity = 0;
  var chosen_circle;
  for (i=0; i< zoom_circles.length; i++) {
    // if it's a lowest-level node, check to see if the first child element beats the current highest similarity
    var current_similarity = zoom_circles[i].__data__.data.children[0].similarity;
    // if so, set a new highest score and save the chosen circle
    if (current_similarity > highest_similarity) {
      highest_similarity = current_similarity;
      chosen_circle = zoom_circles[i].__data__;
    }
  }

  // immediately load the whole viz, but then immediately zoom to the random level-2 cluster
  function zoomOnLoad() {
    zoomTo([root.x, root.y, root.r * 2 + margin]);
    setTimeout(function(){
      // example cluster. will be selected dynamically when in production
      d = chosen_circle;
      zoom(d); //d3.event.stopPropagation();
    }, 500 )
  }

  zoomOnLoad();

  function zoom(d) {
    const focus0 = focus;
    focus = d;
    const transition = d3.transition()
        .duration(750)
        .tween("zoom", d => {
          const i = d3.interpolateZoom(view, [focus.x, focus.y, focus.r * 2 + margin]);
          return t => zoomTo(i(t));
        });
    text
      .filter(function(d) { return d.parent === focus || this.style.display === "inline"; })
      .transition(transition)
        .style("fill-opacity", d => d.parent === focus ? 1 : 0)
        .on("start", function(d) { if (d.parent === focus) this.style.display = "inline"; })
        .on("end", function(d) { if (d.parent !== focus) this.style.display = "none"; });
  }


  function zoomTo(v) {
    var k = diameter / v[2]; view = v;
    node.attr("transform", function(d) { return "translate(" + (d.x - v[0]) * k + "," + (d.y - v[1]) * k + ")"; });
    circle.attr("r", function(d) { return d.r * k; });
  }

}
