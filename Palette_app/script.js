var data = {
    "mode": "transformer", // transformer, diffusion or random
    "num_colors": 5, // max 12, min 2
    "temperature": "1.2", // max 2.4, min 0
    "num_results": 1, // max 50 for transformer, 5 for diffusion
    "adjacency": [], // nxn adjacency matrix as a flat array of strings
    "palette": ["-", "-", "-", "-", "-"]
}

generate();

function generate() {
    let loader = $('.loader')[0];
    loader.style.display = "block";
    data.adjacency = randomAdjacency();

    $.ajax({
        type: "post",
        url: "https://api.huemint.com/color",
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (return_data) {
            var colorarr = [];

            loader.style.display = "none";
            var palette = return_data.results[0].palette;
            console.log(palette)
            let container = document.getElementById("palette-container")
            var colors = $(".color-container")

            for (i in palette) {
                if (data.palette[i] != "-") {
                    colorarr[i] = colors[i]
                }
                else {
                    if (colors[i]) {
                        colors[i].remove();
                    }

                    var colorcontainer = document.createElement("div");
                    colorcontainer.className = 'color-container';
                    let rgb = palette[i][0] + ', ' + palette[i][1] + ', ' + palette[i][2];
                    var color = document.createElement("input");
                    color.type = "color";
                    color.id = "bgcolor"
                    color.className = "color";
                    color.value = palette[i];


                    var colorinfo = document.createElement("div");
                    colorinfo.className = "color-info";

                    var colorrow1 = document.createElement("div");
                    colorrow1.className = "color-info-row";
                    var infokey1 = document.createElement("p");
                    infokey1.innerHTML = "RGB";
                    infokey1.className = "info-key";
                    var infovalue1 = document.createElement("p");
                    infovalue1.innerHTML = hexToRgb(palette[i]);
                    infovalue1.id = "rgb";
                    infovalue1.className = "info-value";

                    colorrow1.appendChild(infokey1);
                    colorrow1.appendChild(infovalue1);

                    var colorrow2 = document.createElement("div");
                    colorrow2.className = "color-info-row";
                    var infokey2 = document.createElement("p");
                    infokey2.innerHTML = "HEX";
                    infokey2.className = "info-key";
                    var infovalue2 = document.createElement("p");
                    infovalue2.innerHTML = palette[i];
                    infovalue2.className = "info-value";
                    infovalue2.id = "hex";

                    colorrow2.appendChild(infokey2);
                    colorrow2.appendChild(infovalue2);

                    var hiddenColor = document.createElement("input");
                    hiddenColor.type = "hidden";
                    hiddenColor.id = "color" + i;
                    hiddenColor.value = palette[i];

                    colorinfo.appendChild(colorrow1);
                    colorinfo.appendChild(colorrow2);
                    colorinfo.appendChild(hiddenColor);

                    var lockcontainer = document.createElement("div");
                    lockcontainer.className = "lock-container";
                    var locktext = document.createElement("p");
                    locktext.innerHTML = "Lock";
                    var lockbox = document.createElement("input");
                    lockbox.type = "checkbox";
                    lockbox.id = "lock";

                    lockcontainer.appendChild(locktext)
                    lockcontainer.appendChild(lockbox)

                    colorcontainer.appendChild(lockcontainer)
                    colorcontainer.appendChild(colorinfo);
                    colorcontainer.appendChild(color);

                    colorarr.push(colorcontainer)
                    // container.appendChild(colorcontainer);

                    color.addEventListener('input', function (e) {
                        // Traverse up the DOM to find the color container for this input
                        let curcontainer = this.parentElement;
                        while (curcontainer && curcontainer.className !== 'color-container') {
                            curcontainer = curcontainer.parentElement;
                        }

                        // Find the infovalue1 and infovalue2 elements within the container
                        let rgbvalue = curcontainer.querySelector('#rgb');
                        let hexvalue = curcontainer.querySelector('#hex');
                        let hiddenColor = curcontainer.querySelector("[type='hidden']");

                        // Update the infovalue1 and infovalue2 elements with the new RGB and hex values
                        rgbvalue.innerHTML = hexToRgb(this.value);
                        hexvalue.innerHTML = this.value;
                        hiddenColor.value = this.value;
                    })
                }
                // if(!container.children[0].querySelector("#lock").checked) {
            }

            for (i in colorarr) {
                container.appendChild(colorarr[i])
            }
            // Run the code here that needs
            //    to access the data returned
            console.log(data);
        },
        error: function () {
            alert('Error occured');
        }
    });
}

function rgbToHex(r, g, b) {
    r = Math.max(0, Math.min(255, r));
    g = Math.max(0, Math.min(255, g));
    b = Math.max(0, Math.min(255, b));
    return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
}

function hexToRgb(hex) {
    // Remove the hash symbol from the beginning of the hex value (if present)
    hex = hex.replace('#', '');

    // Split the hex value into its three component parts (red, green, blue)
    const r = parseInt(hex.substring(0, 2), 16);
    const g = parseInt(hex.substring(2, 4), 16);
    const b = parseInt(hex.substring(4, 6), 16);

    // Return the RGB value as a string
    return r + ', ' + g + ', ' + b;
}

function randomizePalette() {

    var input = [];

    var colors = $(".color-container")
    for (i in colors) {
        if (i >= 0) {
            var lock = colors[i].querySelector("#lock");
            if (lock.checked) {
                var hexstring = colors[i].querySelector("#hex").innerHTML
                input.push(hexstring)
            }
            else {
                input.push("-")
                // colors[i].remove();
            }
        }
    }

    data.palette = input;
    // console.log(data)
    generate();
}

function randomAdjacency() {
    let output = []
    for (let i = 0; i < 25; i++) {
        output.push(Math.round(Math.random() * (50)).toString())
    }
    return output
}