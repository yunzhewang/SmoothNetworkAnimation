function random_graph(){

  var width = 600, height = 500;    // size of svg
  var colors = d3.scaleOrdinal(d3.schemeCategory10);
  var charge = -900;
  var n, m = undefined;      // number of nodes, links
  var link_dist = 120;

  this.init = function(container, node_num, link_num){
      n = node_num; m = link_num;

      var svg = d3.select(container).append("svg")
                  .attr("width", width)
                  .attr("height", height)
                  .on("mousedown", create);

      create();
      function create () {
        svg.selectAll(".links, .nodes").remove();
        randomGraph(svg, node_num, link_num, charge);
      }

  }

      

  function randomGraph (svg, n, m, charge) { //creates a random graph on n nodes and m links

      var nodes = d3.range(n).map(Object);
      // console.log('nodes: ', nodes);

      var list  = randomChoose(unorderedPairs(d3.range(n)), m);
      var links = list.map(function (a) { return {source: a[0], target: a[1]} });
      // console.log('links: ', links);

      // draw graph for verification use (top-right section)
      // nodes and links are loaded from lists
      $('#show_graph').click(function(){ 
        forceLayout.draw("draw_graph", '', nodes, links); 
      });

      var simulation = d3.forceSimulation()
                          .force("link", d3.forceLink().id(function(d) { return d; }).distance(link_dist))
                          .force("charge", d3.forceManyBody())
                          .force("center", d3.forceCenter(width / 2, height / 2));

      var link = svg.append("g")
                    .attr("class", "links")
                    .selectAll("line")
                    .data(links)
                    .enter().append("line")
                    .attr("stroke-width", 3)
                    .attr("stroke", 'grey');

      var node = svg.append("g")
                    .attr("class", "nodes")
                    .selectAll("circle")
                    .data(nodes)
                    .enter().append("circle")
                    .attr("r", 5)
                    .attr("fill", 'white')
                    .call(d3.drag()
                          .on("start", dragstarted)
                          .on("drag", dragged)
                          .on("end", dragended));

      simulation.nodes(nodes)
                .on("tick", tick)
                .on('end', function(){
                    // save the graph data
                    var save_links = [];
                    for(var i=0; i<links.length; i++){
                      var tmp_link = links[i];
                      var weight = n;
                      save_links.push([tmp_link.source.index, tmp_link.target.index, weight])
                    }

                    alert('Layout Accomplished! ');

                    // save
                    $('#save_graph').click(function(){
                      var str = JSON.stringify(save_links);
                      var blob = new Blob([str], {type: "text/plain;charset=utf-8"});
                      saveAs(blob, "data.json");
                    });     
                });


      simulation.force("link")
                .links(links);

      node.transition().duration(800)
          .attr("r", function (d) { 
            var weight = links.filter(function(l) {
                          return l.source.index == d.index || l.target.index == d.index;
            }).length;

            return 3+3*weight; 
          })   
          .style("fill", function (d) { 
            var weight = links.filter(function(l) {
                          return l.source.index == d.index || l.target.index == d.index;
            }).length;

            return colors(weight) 
          });

      link.transition().duration(800)
          .style("stroke-width", 3);

      function tick () {
        node
            .attr("cx", function(d) { return d.x })
            .attr("cy", function(d) { return d.y });

        link
            .attr("x1", function(d) { return d.source.x })
            .attr("y1", function(d) { return d.source.y })
            .attr("x2", function(d) { return d.target.x })
            .attr("y2", function(d) { return d.target.y });
      }
  }



  function randomChoose (s, k) { // returns a random k element subset of s
    var a = [], i = -1, j;
    while (++i < k) {
      j = Math.floor(Math.random() * s.length);
      a.push(s.splice(j, 1)[0]);
    };
    return a;
  }


  function unorderedPairs (s) { // returns the list of all unordered pairs from s
    var i = -1, a = [], j;
    while (++i < s.length) {
      j = i;
      while (++j < s.length) a.push([s[i],s[j]])
    };
    return a;
  }


  function dragstarted(d) {
    d3.event.sourceEvent.stopPropagation();
    d3.select(this).classed("dragging", true);
  }

  function dragged(d) {
    d3.select(this).attr("cx", d.x = d3.event.x).attr("cy", d.y = d3.event.y);
  }

  function dragended(d) {
    d3.select(this).classed("dragging", false);
  }


}



var random_graph = new random_graph();
