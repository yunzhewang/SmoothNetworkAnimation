function force_layout(){

	// var width = 600, height = 500;
	var color = d3.scaleOrdinal(d3.schemeCategory10);
	var charge = -900, link_dist = 60;

	// v3
	this.draw = function(container, filename, g_nodes, g_links){
		var width = document.getElementById(container).clientWidth;
		var height = document.getElementById(container).clientHeight;

		var nodes = [], links = [];

		d3.csv(filename, function(data){
			if(filename != ''){
				console.log('filename: ', filename);
				console.log('data: ', data);
				var links = data.map(function(link){ 
					return {source: link.source, target: link.target, value: link.value}; 
				});

				var nodes = [];
				data.forEach(function(link){
					var src = link.source;  var tar = link.target;
					if(!nodes.includes(src))
						nodes.push(src);
					if(!nodes.includes(tar))
						nodes.push(tar);
				});

				nodes = nodes.map(function(d){ return {'id': d}; });
				
				console.log('nodes: ', nodes);
				console.log('links: ', links);
			}

			if(filename == ''){
				nodes = g_nodes;  links = g_links;
				console.log('nodes: ', nodes);
				console.log('links: ', links);
			}

			var svg = d3.select("#"+container).append("svg")
						.attr('width', width)
						.attr('height', height);

			var simulation = d3.forceSimulation()
							    .force("link", d3.forceLink().id(function(d) { return d.id; }).distance(link_dist))
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
						    .attr("r", 12)
						    .attr("fill", function(d) { return color(d.index); })
						    .call(d3.drag()
						          .on("start", dragstarted)
						          .on("drag", dragged)
						          .on("end", dragended));
			node.append("title")
			    .text(function(d){ return d.index});

			simulation
		      .nodes(nodes)
		      .on("tick", ticked);

		    simulation.force("link")
		      .links(links);

			function ticked() {
			    link
			        .attr("x1", function(d) { return d.source.x; })
			        .attr("y1", function(d) { return d.source.y; })
			        .attr("x2", function(d) { return d.target.x; })
			        .attr("y2", function(d) { return d.target.y; });

			    node
			        .attr("cx", function(d) { return d.x; })
			        .attr("cy", function(d) { return d.y; });
			}

			function dragstarted(d) {
			  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
			  d.fx = d.x;
			  d.fy = d.y;
			}

			function dragged(d) {
			  d.fx = d3.event.x;
			  d.fy = d3.event.y;
			}

			function dragended(d) {
			  if (!d3.event.active) simulation.alphaTarget(0);
			  d.fx = null;
			  d.fy = null;
			}

		});
		
	}
}

var forceLayout = new force_layout();