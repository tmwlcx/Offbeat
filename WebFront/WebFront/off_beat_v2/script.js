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
const redirectUri = 'http://localhost:8888';
const scopes = [
  'user-top-read'
];

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

    console.log(data);
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

          // compute averages
          tracks.audio_features.map(function(song) {
            for (var i in songs) {
              if (songs[i].id == song.id) {
                songs[i].danceability = song.danceability;
                songs[i].energy = song.energy;
                songs[i].speechiness = song.speechiness;
                songs[i].acousticness = song.acousticness;
                songs[i].instrumentalness = song.instrumentalness;
                songs[i].liveness = song.liveness;
                songs[i].valence = song.valence;
                songs[i].tempo = song.tempo;
              }
            }
          });

          var danceability_avg = 0;
          var energy_avg = 0;
          var speechiness_avg = 0;
          var acousticness_avg = 0;
          var instrumentalness_avg = 0;
          var liveness_avg = 0;
          var valence_avg = 0;
          var tempo_avg = 0;

          console.log(songs);
          for (i=0; i<songs.length; i++) {
            danceability_avg += songs[i].danceability;
            energy_avg += songs[i].energy;
            speechiness_avg += songs[i].speechiness;
            acousticness_avg += songs[i].acousticness;
            instrumentalness_avg += songs[i].instrumentalness;
            liveness_avg += songs[i].liveness;
            valence_avg += songs[i].valence;
            tempo_avg += songs[i].tempo;
          }

          var user_averages = {
            'danceability': danceability_avg/num_songs,
            'energy': energy_avg/num_songs,
            'speechiness': speechiness_avg/num_songs,
            'acousticness': acousticness_avg/num_songs,
            'instrumentalness': instrumentalness_avg/num_songs,
            'liveness': liveness_avg/num_songs,
            'valence': valence_avg/num_songs,
            'tempo': tempo_avg/num_songs
          };

          danceability_avg = Math.round(danceability_avg/num_songs * 100);
          energy_avg = Math.round(energy_avg/num_songs * 100);
          speechiness_avg = Math.round(speechiness_avg/num_songs * 100);
          acousticness_avg = Math.round(acousticness_avg/num_songs * 100);
          instrumentalness_avg = Math.round(instrumentalness_avg/num_songs * 100);
          liveness_avg = Math.round(liveness_avg/num_songs * 100);
          valence_avg = Math.round(valence_avg/num_songs * 100);
          tempo_avg = Math.round(tempo_avg/num_songs);

          //
          let structure_html = $('<div class="row" id="profile-row"><div class="col-md-3" id="profile-row-left"></div><div class="col-md-9" id="profile-row-right"></div></div>');
          structure_html.appendTo($('#content'));
          let average_text = $('<p>Your listening profile:</p>');
          average_text.appendTo($('#profile-row-left'));

          $('<ul></ul>').appendTo('#profile-row-left');
          $('<li>danceability: ' + danceability_avg + '%</li>').appendTo('#profile-row-left ul');
          $('<li>energy: ' + energy_avg + '%</li>').appendTo('#profile-row-left ul');
          $('<li>speechiness: ' + speechiness_avg + '%</li>').appendTo('#profile-row-left ul');
          $('<li>acousticness: ' + acousticness_avg + '%</li>').appendTo('#profile-row-left ul');
          $('<li>instrumentalness: ' + instrumentalness_avg + '%</li>').appendTo('#profile-row-left ul');
          $('<li>liveness: ' + liveness_avg + '%</li>').appendTo('#profile-row-left ul');
          $('<li>valence: ' + valence_avg + '%</li>').appendTo('#profile-row-left ul');
          $('<li>tempo: ' + tempo_avg + 'bpm</li>').appendTo('#profile-row-left ul');


          let offbeat_text = $('<p>How offbeat do you want to get?</p>');
          let slider = $('<div class="sliders"><div id="slider-offbeat"></div></div>');
          let explore_button = $('<button onclick="drawGraph()">Explore</button>');
          let user_avg_text = $('<hr></hr><p>[for testing] example of JSON that could be sent to the back end</p>');
          let user_avg_json = $('<pre>' + JSON.stringify(user_averages, undefined, 2) + '</pre>');
          let top_50_json_text = $('<p>[for testing] audio feature data returned for your top ' + num_songs + ' songs from API endpoints:</p>');
          let top_50_json_viewable = $('<pre>' + JSON.stringify(songs, undefined, 2) + '</pre>');

          offbeat_text.appendTo($('#profile-row-left'));
          slider.appendTo($('#profile-row-left'));


          // slider
          var sliderOffbeat = d3
              .sliderBottom()
              .min(0).max(10)
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

          // draw the svg
          let circles = $('<svg id="mychart" width="700" height="700"></svg>');
          circles.appendTo($('#profile-row-right'));

          // print consolidated json data at the bottom of the page
          user_avg_text.appendTo($('#testing'));
          user_avg_json.appendTo($('#testing'));
          top_50_json_text.appendTo($('#testing'));
          top_50_json_viewable.appendTo($('#testing'));

        }
    });

  }
});


function drawGraph() {

    // draw the graph
    var svg = d3.select("#mychart"),
        margin = 20,
        diameter = +svg.attr("width"),
        g = svg.append("g")
            .attr("transform", "translate(" + diameter / 2 + "," + diameter / 2 + ")")
            .attr("id", "mychart-g");

    var color = d3.scaleLinear()
        .domain([-1, 5]) // for depths
        //.range(["hsl(40, 94%, 74%)", "hsl(321, 50%, 40%)"]) // light magma
        .range(["hsl(130, 74%, 73%)", "hsl(112, 72%, 30%)"]) // greens
        .interpolate(d3.interpolateHcl);

    //var colorScale = d3.scaleSequential(d3.interpolateBlues) // for nodes at the very bottomn
    var colorScale = d3.scaleSequential(d3.interpolatePurples) // for nodes at the very bottomn
        .domain([0,1])

    var pack = d3.pack()
        .size([diameter - margin, diameter - margin])
        .padding(2);

    // clear svg elements on redraw
    d3.select("#mychart g").selectAll("circle").remove();
    d3.select("#mychart g").selectAll("text").remove();

    d3.json("test_songs_sample_1k.json").then(function(root) {

        console.log(root);

        root = d3.hierarchy(root)
          .sum(function(d) { return d.size; })
          .sort(function(a, b) { return b.value - a.value; });

        var focus = root,
          nodes = pack(root).descendants(),
          view;

        var circle = g.selectAll("circle")
            .data(nodes)
            .enter().append("circle")
              .attr("class", function(d) { return d.parent ? d.children ? "node" : "node node--leaf" : "node node--root"; })
              .style("fill", function(d) {
                  return d.children ? color(d.depth-1) : colorScale(d.data.similarity);  //"lightgreen";
              })
              .on("click", function(d) {
                  if (focus !== d) {
                      console.log(d);
                      zoom(d), d3.event.stopPropagation();
                  }
              });

        var text = g.selectAll("text")
            .data(nodes)
            .enter().append("text")
              .attr("class", "label")
              .style("fill-opacity", function(d) { return d.parent === root ? 1 : 0; })
              .style("display", function(d) { return d.parent === root ? "inline" : "none"; })
              .text(function(d) { return d.data.hasOwnProperty('similarity') ? "..." + d.data.name.slice(-4) + ": " + d.data.similarity : d.data.name; });

        var node = g.selectAll("circle,text");

        svg
          .on("click", function() { zoom(root); });

        // immediately load the whole viz, but then immediately zoom to a specific cluster
        function zoomOnLoad() {
            zoomTo([root.x, root.y, root.r * 2 + margin]);
            setTimeout(function(){
                // example cluster. will be selected dynamically when in production
                d = {x: 104.79578233413253, y: 320.25745509180723, r:42.94966209781178};
                zoom(d);// d3.event.stopPropagation();
            }, 750 )
        }

        zoomOnLoad();

        function zoom(d) {
            console.log(d);
            var focus0 = focus; focus = d;

            var transition = d3.transition()
                .duration(1250)
                .tween("zoom", function(d) {
                  console.log(focus.x);
                  console.log(focus.y);
                  console.log(focus.r * 2 + margin);
                  var i = d3.interpolateZoom(view, [focus.x, focus.y, focus.r * 2 + margin]);
                  return function(t) { zoomTo(i(t)); };
                });

            transition.selectAll("text")
              .filter(function(d) { return d.parent === focus || this.style.display === "inline"; })
                .style("fill-opacity", function(d) { return d.parent === focus ? 1 : 0; })
                .on("start", function(d) { if (d.parent === focus) this.style.display = "inline"; })
                .on("end", function(d) { if (d.parent !== focus) this.style.display = "none"; });
        }

        function zoomTo(v) {
            var k = diameter / v[2]; view = v;
            node.attr("transform", function(d) { return "translate(" + (d.x - v[0]) * k + "," + (d.y - v[1]) * k + ")"; });
            circle.attr("r", function(d) { return d.r * k; });
        }
    });
}
