/**************************************************************************
 * This script is responsible for managing the frontend interactions of the
 * Elepharma Pipeline Scraper page. It includes logic for:
 *  1) Selecting companies and initiating a scrape
 *  2) Displaying loading animations and error messages
 *  3) Filtering and sorting scraped treatments
 *  4) Generating and downloading CSV files (filtered or full)
 * 
 **************************************************************************/

document.addEventListener('DOMContentLoaded', () => {
    // References to specific DOM elements used throughout
    let foundTreatments = document.getElementById("foundTreatments");
    let currentlyEmpty = document.getElementById("currentlyEmpty");
    let sortMenu = document.getElementById("sortMenu");
    let csvDownload = document.getElementById("csvDownload");

    // Variables used throughout different sections
    let allTreatmentsData = [];
    let currentFilteredTreatments = [];
    let lastColumnSorted = "phase";
    let sortForGrid = "asc";
    let sortFilterDirections = {
        treatment_name: "asc",
        company: "asc",
        therapeutic_area: "asc",
        indication: "asc",
        phase: "asc"
    }


    /*************************************************************************
     *                         Dropdown Menu Functions                       *
     *************************************************************************/
    let dropdownButton = document.getElementById("dropdownButton");
    let fullList = document.getElementById("fullList");
    let selectEveryCompany = document.getElementById("selectEveryCompany");

    dropdownButton.addEventListener('click', () => {
        fullList.classList.toggle('showCompanies');
        dropdownButton.classList.toggle('currentlyOn');
    });

    // Create a select all button in the dropdown menu
    let individualCompanyBoxes = 
        document.querySelectorAll('input[name="nextCompany"]');

    selectEveryCompany.addEventListener('change', () => {
        individualCompanyBoxes.forEach(nextBox => {
            nextBox.checked = selectEveryCompany.checked;
        });

        updatedDropdownButtonText()
    });

    // Add event listeners to each box in the dropdown menu
    individualCompanyBoxes.forEach(nextBox => {
        nextBox.addEventListener("change", () => {
            let checkAllBoxesTrue = 
            [...individualCompanyBoxes].every(box => box.checked);

            let checkAllBoxesFalse =         
            [...individualCompanyBoxes].every(box => !box.checked);

            if (checkAllBoxesTrue) {
                individualCompanyBoxes.checked = true;
            } else if (checkAllBoxesFalse) {
                individualCompanyBoxes.checked = false;
            } else {
                individualCompanyBoxes.checked = false;
            }
        });
    });
    
    document.addEventListener('change', (foundEvent) => {
        if (foundEvent.target.matches('input[name="nextCompany"]')) {
            updatedDropdownButtonText();
        }
    });

    // Update the text in the button for the dropdown menu to contain the
    // companies chosen
    function updatedDropdownButtonText() {
        let foundBoxes = document.querySelectorAll('input[name="nextCompany"]');
        let chosenCompanies = [];
        foundBoxes.forEach((selected) => {
            if (selected.checked) {
                chosenCompanies.push(selected.parentElement.textContent.trim());
            }
        });

        // Change the text based on how many companies are selected by
        // the user/client
        if (chosenCompanies.length == 0) {
            dropdownButton.textContent = 'Select Companies';
        } else if (chosenCompanies.length <= 2) {
            dropdownButton.textContent = chosenCompanies.join(', ');
        } else {
            dropdownButton.textContent = `${chosenCompanies.length}` +
                                          ` companies selected`;
        }
    }
    updatedDropdownButtonText();


    /*************************************************************************
     *                          Main Scrape Function                         *
     *************************************************************************/
    let scrapingButton = document.getElementById("startScrapingButton");
    let loadingAni = document.getElementById("loadingAni");
    let loadingMessage = document.getElementById("loadingMessage");
    let noConnection = document.getElementById("noConnection");
    let rowWithFilters = document.getElementById("rowWithFilters");

    // When the user clicks 'Scrape', we grab the selected companies and
    // trigger the backend scrape process
    scrapingButton.addEventListener('click', scrape);
    async function scrape() {
        let foundBoxes = document.querySelectorAll('input[name="nextCompany"]'
                                                   + ':checked');
        let finalCompanies =  Array.from(foundBoxes).map(curr => curr.value);

        if (finalCompanies.length == 0) {
            alert('Please select at least one company!');
            return;
        }

        // Hide the "Download CSV" button, initial landing page/errors, and
        // filter bar
        csvDownload.classList.remove("complete-download");
        document.getElementById("landing").style.display = "none";
        noConnection.classList.remove("showNoConnection");
        currentlyEmpty.classList.remove("showEmpty");
        rowWithFilters.classList.remove('showFilters');
        listHeader.style.display = "none";

        scrapingButton.removeEventListener("click", scrape);
        scrapingButton.className = "waiting";

        foundTreatments.innerHTML = "";
        allTreatmentsData = []

        // Show the landing animation
        loadingAni.classList.add('showLoading');
        loadingMessage.classList.add("showFirstMessage");
        loadingMessage.textContent = "Currently scraping treatments...";

        /*
         * Change the loading animation being shown based on the amount
         * of time it takes to finish the scraping
         */
        function changeLoadingMessage() {
            loadingMessage.classList.remove("showFirstMessage");
            loadingMessage.classList.add("showSecondMessage");
            loadingMessage.textContent = "Still scraping...";

            trackMessage = setTimeout(() => {
                loadingMessage.classList.remove("showSecondMessage");
                loadingMessage.classList.add("showThirdMessage");
                loadingMessage.textContent = "Almost there...";
            }, 10000);
        }
        let trackMessage = setTimeout(changeLoadingMessage, 5000);

        try {
            // Post the selected companies to the /scrape endpoint
            let grabbedResponse = await fetch('/scrape', {
                method: 'POST',
                headers: {'Content-Type': 'text/plain'},
                body: JSON.stringify(finalCompanies)
            });

            if (!grabbedResponse.ok) {
                throw new Error(`ERROR! Status: ${grabbedResponse.status}`);
            }

            uid = await grabbedResponse.text()

            // For each selected company, fetch partial results from
            // the backend by doing a GET request to /get_response
            for (let i = 0; i < finalCompanies.length; i++) {
                let res = await fetch('/get_response', 
                                      {method: 'POST', body: uid});

                if (!res.ok) {
                    throw new Error(`ERROR! Status: ${res.status}`);
                }

                let text = await res.text();

                // Need to update the user/client once results start
                // coming in
                if (i == 0) {
                    clearTimeout(trackMessage);
                    loadingMessage.innerHTML = "";
                    loadingAni.classList.remove('showLoading');
                    initializeStatusBar(finalCompanies);
                }
                
                // Need to update the user on the current status of each
                // individual company that was scraped
                for (let comp of finalCompanies) {
                    if (text.toLowerCase().includes(comp.toLowerCase())) {
                        statusUpdateForIndividualCompany(comp, text);
                        break;
                    }
                }
            }

            // Finally, retrieve the full dataset from the backend
            let final = await fetch('/get_final',
                                    {method: 'POST', body: uid});
            if (!final.ok) {
                throw new Error(`ERROR! Status: ${final.status}`);
            }
            grabbedData = await final.json();

            // Get the csv file and save the response globally as a blob
            let csv_response = await fetch('/download_csv',
                                           {method: 'POST', body: uid});
            if (!csv_response.ok) {
                throw new Error(`ERROR! Status: ${csv_response.status}`);
            }
            savedCSV = await csv_response.blob();
            
            status_elem = document.getElementById('statusBarContainer');
            status_elem.classList.remove("statusBarReveal");

            // Store all of the data into a variable that we can use later
            allTreatmentsData = grabbedData;
            currentFilteredTreatments = grabbedData;

            populateAllFilters(grabbedData);
            resetHeaders();
            rowWithFilters.classList.add('showFilters');
            sortFilterHeader("treatment_name", true);
            sortFilterHeader("phase", true);
        } catch (error) {
            clearTimeout(trackMessage);
            console.error(error);
            loadingAni.classList.remove("showLoading");
            noConnection.classList.add("showNoConnection");
        } finally {
            scrapingButton.addEventListener("click", scrape);
            scrapingButton.className = "";
        }
    }


    /*************************************************************************
     *                          CSV Download Functions                       *
     *************************************************************************/
    let savedCSV;

    /* Create and trigger a download of the 'currentFilteredTreatments' in a
     * CSV file. Specifically used when the user applies filters and wants a
     * partial CSV.
     */
    function downloadFilteredCSV() {
        let csvTreatmentContent = "data:text/csv;charset=utf-8,";
        csvTreatmentContent += "Company,Treatment_Name,Therapeutic_Area," + 
                            "Indication,Phase\n";

        // Convert each filtered treatment into a CSV row
        currentFilteredTreatments.forEach(nextTreatment => {
            let nextRow = [
                nextTreatment.company || "N/A",
                nextTreatment.treatment_name || "N/A",
                nextTreatment.therapeutic_area || "N/A",
                nextTreatment.indication || "N/A",
                nextTreatment.phase || "N/A",
            ];

            // Escape fields with quotes, commas, or line breaks by wrapping
            // them in quotes and doubling internal quotes
            let formattedNextRow = nextRow.map(nextValue => {
                if (nextValue.includes(',') || nextValue.includes('"')
                    || nextValue.includes('\n')) {
                    return `"${nextValue.replace(/"/g, '""')}"`;
                }
                
                return nextValue;
            }).join(',');

            csvTreatmentContent += formattedNextRow + "\n";
        });

        let encodedUri = encodeURI(csvTreatmentContent);

        // Create a temporary <a> element to trigger the download
        let csvLink = document.createElement("a");
        csvLink.setAttribute("href", encodedUri);
        csvLink.setAttribute("download", "treatment_output.csv");

        csvLink.click();
        document.body.removeChild(csvLink);
    }

    /* If the user has applied filters, generate a filtered CSV client-slide.
     * Otherwise, redirect to the server's /download_Csv route to retrieve the
     * full CSV
     */
    function downloadFinalCSV() {
        let chosenFilters =
            filterByCompany.value != "allCompanies" ||
            filterByPhase.value != "allPhases" ||
            specificTextInput.value.trim() != "";

        if (chosenFilters) {
            downloadFilteredCSV();
        } else {
            // Create a temporary <a> element to trigger the download
            let csvLink = document.createElement("a");
            let url = window.URL.createObjectURL(savedCSV);
            csvLink.setAttribute("href", url);
            csvLink.setAttribute("download", "treatment_output.csv");

            csvLink.click();
            window.URL.revokeObjectURL(url);
        }
    }
    document.getElementById("csvDownload").onclick = downloadFinalCSV;


    /*************************************************************************
     *                          Visualize Functions                          *
     *************************************************************************/
    let listView = document.getElementById("listToggle");
    let gridView = document.getElementById("gridToggle");
    let listHeader = document.getElementById("listHeader");

    /* Display the provided treatments on the page, either in a list view
     * or grid view. Also handle empty states and enabling the CSV
     * download button if relevant
     */
    function showTreatments(allTreatments) {
        foundTreatments.innerHTML = "";

        // Show "No Treatments Found" message if we get an empty array
        if (!allTreatments || allTreatments.length == 0) {
            currentlyEmpty.classList.add("showEmpty");
            csvDownload.classList.remove("complete-download");
            return;
        }

        currentlyEmpty.classList.remove("showEmpty");
        csvDownload.classList.add("complete-download");
        foundTreatments.style.display = "flex";

        if (foundTreatments.className == "listView") {
            listHeader.style.display = "flex";
        }

        // For each treatment, build a card-like element and append
        // it to the container
        allTreatments.forEach(nextTreatment => {
            let nextCard = document.createElement('div');
            nextCard.className = 'nextTreatmentCard'
            nextCard.innerHTML = `
            <h3>${nextTreatment.treatment_name}</h3>
            <p><strong>Company:</strong>${nextTreatment.company}</p>
            <p><strong>Therapeutic Area:</strong>\
            ${nextTreatment.therapeutic_area}</p>
            <p><strong>Indication:</strong>${nextTreatment.indication}</p>
            <p><strong>Phase:</strong>${nextTreatment.phase}</p>
            `;
            foundTreatments.appendChild(nextCard);
        });
    }

    // Switch the container to list view mode, reveal the header row
    listView.addEventListener('click', () => {
        foundTreatments.className = "listView";
        if (foundTreatments.innerHTML != "") {
            listHeader.style.display = "flex";
        }

        let sortMenuDiv = document.getElementById("sortDropdown");
        sortMenuDiv.style.display = "none";
        listView.style.backgroundColor = "#0e5d9d";
        gridView.style.backgroundColor = "#2196F3";
    });

    // Switch the container to grid view mode, and hide the header row
    gridView.addEventListener('click', () => {
        foundTreatments.className = "gridView";
        listHeader.style.display = "none";
        gridView.style.backgroundColor = "#0e5d9d";
        listView.style.backgroundColor = "#2196F3";

        let sortMenuDiv = document.getElementById("sortDropdown");
        sortMenuDiv.style.display = "flex";

        // Change sort option in dropdown to the same as lastColumnSorted
        let allOptions = sortMenu.options;
        for (var i = 0; i < allOptions.length; i++) {
            allOptions[i].innerText = allOptions[i].value;
            if (allOptions[i].getAttribute("key") == lastColumnSorted) {
                allOptions[i].selected = true;
            }
        }

        // Change the sorting direction for the grid view
        sortForGrid = sortFilterDirections[selectedHeader];
        if (sortForGrid == "desc") {
            arrowForGrid.classList.add("makeDesc");
        } else {
            arrowForGrid.classList.remove("makeDesc");
        }
        
        // Change text of selected to be prefixed by "Sort: "
        let selected = allOptions[allOptions.selectedIndex]
        selectedHeader = selected.getAttribute("key");
        selected.innerText = "Sort: " + selected.value;
    });


    /*************************************************************************
     *                            Filter Functions                           *
     *************************************************************************/
    let filterByCompany = document.getElementById("filterByCompany");
    let filterByCategory = document.getElementById("filterByCategory");
    let filterByPhase = document.getElementById("filterByPhase");
    let clearAllFilters = document.getElementById("clearAllFilters");
    let specificTextInput = document.getElementById("specificTextInput");
    let removeCriteria = document.getElementById("removeCriteria");
    
    // Populate the filter dropdowns (company & phase) based on the data 
    // that has been returned from the scrapes
    function populateAllFilters(grabbedTreatments) {
        filterByCompany.innerHTML = '<option value="allCompanies">' + 
                                    'All Companies</option>'
        filterByPhase.innerHTML = '<option value="allPhases">All Phases' + 
                                  '</option>'

        // Collect all unique companies and unique phases
        let foundCompanies = [...new Set(grabbedTreatments.map(nextTreatment =>
            nextTreatment.company))]
        let foundPhases = [...new Set(grabbedTreatments.map(nextTreatment =>
            nextTreatment.phase))]

        // Sort both the companies and phases so as to make it easier
        // for the user/client to understand
        foundCompanies.sort();
        foundPhases.sort((a, b) => {
            let priorityA = getPhasePriority(a)
            let priorityB = getPhasePriority(b)

            if (priorityA > priorityB) {
                return 1;
            } else if (priorityB > priorityA) {
                return -1;
            } else {
                return 0;
            }
        });

        // Populate the company dropdown menu
        foundCompanies.forEach(nextCompany => {
            let nextOption = document.createElement('option');
            nextOption.value = nextCompany;
            nextOption.textContent = nextCompany;
            filterByCompany.appendChild(nextOption);
        });


        // Populate the phase dropdown menu
        foundPhases.forEach(nextPhase => {
            let nextOption = document.createElement('option');
            nextOption.value = nextPhase;
            nextOption.textContent = nextPhase;
            filterByPhase.appendChild(nextOption);
        });
    }

    /* Filters the treatments based on the user's current selections
     * (chosen company, category, phase, and text). Then updates
     * the displayed treatments accordingly
     */
    function useSelectedFilters() {
        let chosenCompany = filterByCompany.value;
        let chosenCategory = filterByCategory.value;
        let chosenPhase = filterByPhase.value;
        let givenText = specificTextInput.value.toLowerCase().trim();

        let filteredTreatments = [...allTreatmentsData];

        // Filter by chosen company if not 'allCompanies' (in HTML)
        if (chosenCompany != 'allCompanies') {
            filteredTreatments = filteredTreatments.filter(nextTreatment =>
                nextTreatment.company == chosenCompany
            );
        }

        // Filter by chosen phase if not 'allPhases' (in HTML)
        if (chosenPhase != 'allPhases') {
            filteredTreatments = filteredTreatments.filter(nextTreatment =>
                nextTreatment.phase == chosenPhase
            );
        }

        // Filter by user-entered text in the chosenCategory field
        if (givenText) {
            filteredTreatments = filteredTreatments.filter(nextTreatment => {
                let val = nextTreatment[chosenCategory]?.toLowerCase() || '';
                return val.includes(givenText);
            });
        }

        currentFilteredTreatments = filteredTreatments;
        showTreatments(filteredTreatments);
        
        // Make sure to maintain the active sorted column
        if (lastColumnSorted) {
            sortFilterHeader(lastColumnSorted, true);
        }
    }

    // Connect filtering logic with event listeners
    filterByCompany.addEventListener('change', useSelectedFilters);
    filterByCategory.addEventListener('change', useSelectedFilters);
    filterByPhase.addEventListener('change', useSelectedFilters);

    specificTextInput.addEventListener('input', function() {
        if (this.value) {
            removeCriteria.classList.add('showCriteriaButton');
        } else {
            removeCriteria.classList.remove('showCriteriaButton');
        }

        useSelectedFilters();
    });

    removeCriteria.addEventListener('click', function() {
        specificTextInput.value = '';
        removeCriteria.classList.remove('showCriteriaButton');
        useSelectedFilters();
    });

    // Clear all the current filters and reset them to their default values
    clearAllFilters.addEventListener('click', () => {
        filterByCompany.value = 'allCompanies';
        filterByPhase.value = 'allPhases';
        filterByCategory.value = 'therapeutic_area';

        specificTextInput.value = '';
        removeCriteria.classList.remove('showCriteriaButton');

        useSelectedFilters();

        // Make sure to maintain the active sorted column
        if (lastColumnSorted) {
            sortFilterHeader(lastColumnSorted, true);
        }
    });


    /*************************************************************************
     *                          Sorting Functions                            *
     *************************************************************************/
    let arrowForGrid = document.getElementById("arrowForGrid");
    let treatmentNameHeader = document.getElementById("treatmentNameHeader");
    let companyHeader = document.getElementById("companyHeader");
    let therapeuticHeader = document.getElementById("therapeuticAreaHeader");
    let indicationHeader = document.getElementById("indicationHeader");
    let phaseHeader = document.getElementById("phaseHeader");

    /* Given the phase of the treatment, as a string, give it a number priority
     * for sorting. A lower priority means that when sorted by ascending, it
     * appears closer towards the top of the page
     */
    function getPhasePriority(phase) {
        switch (phase) {
            case "Approved":
                return 0;
            case "Phase 3":
                return 1;
            case "Phase 2":
                return 2;
            case "Phase 1":
                return 3;
            case "Preclinical":
                return 4;
            default:
                return 100;
        }
    }

    // Add event listeners to the list view headers so when clicked
    // we can sort the treaments on command
    treatmentNameHeader.addEventListener("click", () => {
        className = treatmentNameHeader.className;
        noChangeDir = true;

        if (className != "") {
            noChangeDir = false;   
        }
        sortFilterHeader("treatment_name", noChangeDir);
    });

    companyHeader.addEventListener("click", () => {
        className = companyHeader.className;
        noChangeDir = true;

        if (className != "") {
            noChangeDir = false;   
        }
        sortFilterHeader("company", noChangeDir);
    });

    therapeuticHeader.addEventListener("click", () => {
        className = therapeuticHeader.className;
        noChangeDir = true;

        if (className != "") {
            noChangeDir = false;   
        }
        sortFilterHeader("therapeutic_area", noChangeDir);
    });

    indicationHeader.addEventListener("click", () => {
        className = indicationHeader.className;
        noChangeDir = true;

        if (className != "") {
            noChangeDir = false;   
        }
        sortFilterHeader("indication", noChangeDir);
    });

    phaseHeader.addEventListener("click", () => {
        className = phaseHeader.className;
        noChangeDir = true;

        if (className != "") {
            noChangeDir = false;   
        }
        sortFilterHeader("phase", noChangeDir);
    });

    // Change text for selected choice in sort dropdown to start with "Sort: "
    sortMenu.addEventListener("change", () => {
        let allOptions = sortMenu.options;
        for (let i = 0; i < allOptions.length; i++) {
            allOptions[i].innerText = allOptions[i].value;   
        }

        let selected = allOptions[allOptions.selectedIndex]
        selectedHeader = selected.getAttribute("key");

        let findDirNow = sortForGrid;
        sortFilterDirections[selectedHeader] = findDirNow;

        if (findDirNow == "desc") {
            arrowForGrid.classList.add("makeDesc");
        } else {
            arrowForGrid.classList.remove("makeDesc");
        }

        selected.innerText = "Sort: " + selected.innerHTML;
        if (currentFilteredTreatments.length != 0) {
            sortFilterHeader(selectedHeader, true);
        }
    });
    sortMenu.dispatchEvent(new Event("change"));

    /* Sorts the currently shown treatments by the specified column
     * and toggels the direction between ascending and descending,
     * while also re-rendering the treamtnets shown to the user/client
     * and updates the column arrow columns
     */
    function sortFilterHeader(selectedHeader, noToggle = false) {
        let currentSortState = sortFilterDirections[selectedHeader];
        let currDir = currentSortState;

        // If needed flip arrow to the opposite direction
        if (!noToggle) {
            if (currentSortState == "asc") {
                currDir = "desc";
            } else {
                currDir = "asc";
            }
        }
        
        sortFilterDirections[selectedHeader] = currDir;
        lastColumnSorted = selectedHeader;

        // Phase needs to be sorted in non-alphabetic so give it a special case
        if (lastColumnSorted == "phase") {
            currentFilteredTreatments.sort((first, second) => {
                let firstPriority = getPhasePriority(first[selectedHeader])
                let secondPriority = getPhasePriority(second[selectedHeader])
                
                return compareFields(firstPriority, secondPriority, currDir);
            });
        } else {
            currentFilteredTreatments.sort((first, second) => {
                let firstField = (first[selectedHeader] || "").toLowerCase();
                let secondField = (second[selectedHeader] || "").toLowerCase();
                
                return compareFields(firstField, secondField, currDir);
            });
        }
        
        // Re-render the treatments shown to the user/client
        // and avoid reverting back to our default sorting technique
        showTreatments(currentFilteredTreatments);
        changeFilterArrows(selectedHeader);
    }

    // Compare the fields given using alphabetical order, taking into account
    // whether it is descending or ascending order
    // Negative means first comes before, positive means first comes after,
    // and 0 means they are equal
    function compareFields(firstField, secondField, dir) {
        if (firstField < secondField) {
            if (dir == "asc") {
                return -1; // first value comes before second value
            } else {
                return 1; // second value comes before first value
            }
        }

        if (firstField > secondField) {
            if (dir == "asc") {
                return 1;
            } else {
                return -1;
            }
        }
        
        return 0;
    }
    
    // Update the arrow icons on the filter headers, while
    // also reseting the non-chosen filter columns to the default
    function changeFilterArrows(selectedHeader) {
        let foundHeaders = {
            treatment_name: "treatmentNameHeader",
            company: "companyHeader",
            therapeutic_area: "therapeuticAreaHeader",
            indication: "indicationHeader",
            phase: "phaseHeader"
        }
        
        // Loop through each possible column header and update
        // the arrow directions accordingly
        for (let nextHeader in foundHeaders) {
            let foundHeader = document.getElementById(foundHeaders[nextHeader]);
            let arrow = foundHeader.querySelector(".sortFilterArrow");
            if (!foundHeader || !arrow) {
                continue
            }

            // Remove currently active sorted column styles
            foundHeader.classList.remove("sortFilterActAsc");
            foundHeader.classList.remove("sortFilterActDesc");

            if (nextHeader == selectedHeader) {
                // Update content if specific column was clicked
                if (sortFilterDirections[nextHeader] == "asc") {
                    arrow.textContent = "▲";
                    foundHeader.classList.add("sortFilterActAsc");
                } else {
                    arrow.textContent = "▼";
                    foundHeader.classList.add("sortFilterActDesc");
                }
            }
        }
    }

    // Change sort direction while in the grid view
    arrowForGrid.addEventListener("click", () => {
        let currentSort = sortMenu[sortMenu.selectedIndex];
        let currentColumn = currentSort.getAttribute("key");

        if (sortForGrid == "asc") {
            sortFilterDirections[currentColumn] = "desc";
            arrowForGrid.classList.add("makeDesc");
            sortForGrid = "desc";
        } else {
            sortFilterDirections[currentColumn] = "asc";
            arrowForGrid.classList.remove("makeDesc");
            sortForGrid = "asc";
        }

        lastColumnSorted = currentColumn;
        sortFilterHeader(currentColumn, true);
    });

    // Reset the sort directions of all headers to asc
    function resetHeaders() {
        lastColumnSorted = "phase";
        sortForGrid = "asc";

        for (let key in sortFilterDirections) {
            sortFilterDirections[key] = "asc";
        }
    }


    /*************************************************************************
     *                          Status Bar Functions                         *
     *************************************************************************/

    // Set the status bar back to the initial state (all gray) and show
    function initializeStatusBar(incomingCompanies) {
        let statusBarContainer = document.getElementById("statusBarContainer");
        let statusBarID = document.getElementById("statusBarIdentifier");
        let statusBarCompanies = document.getElementById("statusBarCompanies");

        statusBarContainer.classList.add("singleBar");

        statusBarCompanies.innerHTML = "";
        statusBarID.innerHTML = "";
        
        // Loop through each company in order to create individual elements that
        // will make up the status bar
        incomingCompanies.forEach(nextCompany => {
            let nextStatusPiece = document.createElement("div");
            nextStatusPiece.className = 'statusBarIndividualCompanies';
            nextStatusPiece.setAttribute('nextBarCompany', nextCompany);
            statusBarCompanies.appendChild(nextStatusPiece);

            // Create the next individual identifier of the status bar
            // which includes the company name
            let nextStatusPieceID = document.createElement("div");
            nextStatusPieceID.className = "statusBarIndividualIdentifier";
            nextStatusPieceID.textContent = nextCompany.toUpperCase();
            nextStatusPieceID.setAttribute('nextBarCompany', nextCompany);
            statusBarIdentifier.appendChild(nextStatusPieceID);
        });

        statusBarContainer.classList.add("statusBarReveal");
    }

    // Update a single section section of the status bar
    function statusUpdateForIndividualCompany(nextCompany, nextUpdate) {
        // Grab the individual piece of the status bar we want
        q1 = `.statusBarIndividualCompanies[nextBarCompany="${nextCompany}"]`;
        let nextStatusPiece = document.querySelector(q1);
        q2 = `.statusBarIndividualIdentifier[nextBarCompany="${nextCompany}"]`;
        let nextStatusIdentifier = document.querySelector(q2);

        nextStatusPiece.classList.add("allDone");
        nextStatusIdentifier.classList.add("allDone");

        // Update text under status bar
        let foundCorrectUpdate = nextUpdate.match(/(\d+)/);
        let text = `${nextCompany.toUpperCase()}:\n(${foundCorrectUpdate[1]})`;
        nextStatusIdentifier.textContent = text;
    }
});