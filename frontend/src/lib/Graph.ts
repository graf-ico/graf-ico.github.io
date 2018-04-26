import * as d3 from 'd3';
// import * as scale from 'd3-scale';


function countToRadius(count: number): number {
    return Math.log2(count / 3) * 10
}

function overlapToDistance(overlap: number, leftSize: number, rightSize: number): number {
    // overlap is in range [0..100]

    return (countToRadius(leftSize) + countToRadius(rightSize)) + ((100 - overlap) ** 3) / 500
}

function dragstarted(d: any) {
    if (!d3.event.active) {
        simulation.alphaTarget(0.3).restart();
    }
    d.fx = d.x;
    d.fy = d.y;
}

function dragged(d: any) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
}

function dragended(d: any) {
    if (!d3.event.active) {
        simulation.alphaTarget(0);
    }
    d.fx = null;
    d.fy = null;
}

function pythag(r: number, b: number, coord: number) {
    return coord;
    // // // force use of b coord that exists in circle to avoid sqrt(x<0)
    // // b = Math.min(RADIUS * 2 - r - STROKE_WIDTH, Math.max(r + STROKE_WIDTH, b));

    // // const b2 = Math.pow((b - RADIUS), 2);
    // // const a = Math.sqrt(RADIUS * RADIUS - b2);

    // // // radius - sqrt(hyp^2 - b^2) < coord < sqrt(hyp^2 - b^2) + radius
    // // coord = Math.max(RADIUS - a + r + STROKE_WIDTH,
    // //     Math.min(a + RADIUS - r - STROKE_WIDTH, coord));

    // // return coord;
}


function ticked(nodeP: any, imgP: any) {
    nodeP
        .attr("cx", (d: any) => {
            return d.x = pythag(countToRadius(d.size), d.y, d.x)
        })
        .attr("cy", (d: any) => {
            return d.y = pythag(countToRadius(d.size), d.x, d.y)
        });

    link
        // tslint:disable-next-line:no-console
        .attr("x1", (d: any) => { console.log(d.source.x); return d.source.x })
        .attr("y1", (d: any) => d.source.y)
        .attr("x2", (d: any) => d.target.x)
        .attr("y2", (d: any) => d.target.y);

    // tslint:disable-next-line:no-console
    imgP.attr("x", (d: any) => d.x - countToRadius(d.size));
    imgP.attr("y", (d: any) => d.y - countToRadius(d.size));
}



let svg: any;
let simulation: d3.Simulation<{}, any>;
let link: any = null;

let linkGroup: any = null;
let forcelinks: any;

export function initialise(nodes: any[], callback: (group: string) => void) {

    svg = d3.select('#graph-svg').attr("width", "100%")
        .attr("height", "100%")
        .call(d3.zoom().scaleExtent([0.2, 4]).on("zoom", () => {
            svg.attr("transform", d3.event.transform)
        }))
        .append("g");

    const width = +svg.attr("width");
    const height = +svg.attr("height");


    const RADIUS = 5000;
    const STROKE_WIDTH = 9
    // Bounding ring
    svg.append('circle')
        .attr("stroke", "black")
        .attr("stroke-width", STROKE_WIDTH * 2)
        .attr("fill", "rgba(0,0,0,0)")
        .attr("r", RADIUS)
    // .attr('translate(' + w / 2 + ',' + h / 2 + ')');

    // const color = d3.scaleOrdinal(d3.schemeCategory10);

    simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id((d: any) => d.id))
        .force("charge", d3.forceManyBody().strength(-1400))
        .force("center", d3.forceCenter(width / 2, height / 2));


    linkGroup = svg.append("g")
        .attr("class", "links")
        .selectAll("line")
    link = linkGroup
        .data([]);


    const divs = svg.append("g")
        .attr("class", "nodes")
        .selectAll("circle")
        .data(nodes)
        .enter().append('g')
        .attr("height", 50)
        .attr("width", 50);
    // .append('div')
    // .attr("height", 100)
    // .attr("width", 100)

    const img = divs.append("svg:image")
        .attr("xlink:href", (d: any) => {
            try {
                return require('../../public/logos/' + d.id + '.png')
            } catch (err) {
                return ""
            }
            // "/" + d.id + ".jpg"
        })
        .attr("height", (d: any) => 2 * countToRadius(d.size))
        .attr("width", (d: any) => 2 * countToRadius(d.size));

    const node = divs.append("circle")
        .attr("r", (d: any) => countToRadius(d.size))
        .attr("stroke", "black")
        .attr("stroke-width", 5)
        .attr("fill", "rgba(0,0,0,0)")
        .on("click", (d: any) => callback(d.id))
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));


    forcelinks = simulation.force("link")
    if (forcelinks) {
        forcelinks.links([]).distance((lnk: any) => lnk.distance);
    }

    // node;

    node.append("title")
        .text((d: any) => d.id);

    simulation
        .nodes(nodes)
        .on("tick", () => ticked(node, img));
}

export function render(main: any, others: any[]) {

    const links = others.filter((entry: any) => entry.overlap > 0).map((entry: any) => ({ "source": main.id, "target": entry.id, "distance": overlapToDistance(entry.overlap, entry.size, main.size), "size": entry.size }))

    linkGroup.exit().remove();

    link = linkGroup.data(links)
        .enter().append("line")
        .attr("stroke", "black")
        .attr("stroke-width", 2);

    forcelinks.links(links).distance((lnk: any) => lnk.distance);
}