var svg = d3.select("svg"),
    margin = 20,
    diameter = +svg.attr("width"),
    g = svg.append("g").attr("transform", "translate(" + diameter / 2 + "," + diameter / 2 + ")");

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

function drawGraph() {

    d3.json("test_songs_sample_1k.json").then(function(root) {

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
              .on("click", function(d) { if (focus !== d) zoom(d), d3.event.stopPropagation(); });

        var text = g.selectAll("text")
            .data(nodes)
            .enter().append("text")
              .attr("class", "label")
              .style("fill-opacity", function(d) { return d.parent === root ? 1 : 0; })
              .style("display", function(d) { return d.parent === root ? "inline" : "none"; })
              .text(function(d) { return d.data.hasOwnProperty('similarity') ? "..." + d.data.name.slice(-4) + ": " + d.data.similarity : d.data.name; });

        var node = g.selectAll("circle,text");

        svg
          //.style("background", color(-1))
          .on("click", function() { zoom(root); });

        zoomTo([root.x, root.y, root.r * 2 + margin]);

        function zoom(d) {
            var focus0 = focus; focus = d;

            var transition = d3.transition()
                .duration(d3.event.altKey ? 7500 : 750)
                .tween("zoom", function(d) {
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

drawGraph();

// all sliders
var sliderData = [0,1,2,3,4,5,6,7,8,9,10];

// slider-offbeat
var sliderOffbeat = d3
    .sliderBottom()
    .min(0).max(10)
    .step(1)
    .width(200)
    .default(9)
var gTime = d3
    .select('div#slider-offbeat').append('svg')
    .attr('width', 250).attr('height', 70)
    .append('g')
    .attr('transform', 'translate(20,30)');
gTime.call(sliderOffbeat);

// slider-energy
var sliderEnergy = d3
    .sliderBottom()
    .min(0).max(10)
    .step(1)
    .width(200)
    .default(Math.floor(Math.random() * 11))
var gTime = d3
    .select('div#slider-energy').append('svg')
    .attr('width', 250).attr('height', 60)
    .append('g')
    .attr('transform', 'translate(20,20)');
gTime.call(sliderEnergy);

// slider-acousticness
var sliderAcousticness = d3
    .sliderBottom()
    .min(0).max(10)
    .step(1)
    .width(200)
    .default(Math.floor(Math.random() * 11))
var gTime = d3
    .select('div#slider-acousticness').append('svg')
    .attr('width', 250).attr('height', 60)
    .append('g')
    .attr('transform', 'translate(20,20)');
gTime.call(sliderAcousticness);

// slider-danceability
var sliderDanceability = d3
    .sliderBottom()
    .min(0).max(10)
    .step(1)
    .width(200)
    .default(Math.floor(Math.random() * 11))
var gTime = d3
    .select('div#slider-danceability').append('svg')
    .attr('width', 250).attr('height', 60)
    .append('g')
    .attr('transform', 'translate(20,20)');
gTime.call(sliderDanceability);

// slider-instrumentalness
var sliderInstrumentalness = d3
    .sliderBottom()
    .min(0).max(10)
    .step(1)
    .width(200)
    .default(Math.floor(Math.random() * 11))
var gTime = d3
    .select('div#slider-instrumentalness').append('svg')
    .attr('width', 250).attr('height', 60)
    .append('g')
    .attr('transform', 'translate(20,20)');
gTime.call(sliderInstrumentalness);

// slider-valence
var sliderValence = d3
    .sliderBottom()
    .min(0).max(10)
    .step(1)
    .width(200)
    .default(Math.floor(Math.random() * 11))
var gTime = d3
    .select('div#slider-valence').append('svg')
    .attr('width', 250).attr('height', 60)
    .append('g')
    .attr('transform', 'translate(20,20)');
gTime.call(sliderValence);