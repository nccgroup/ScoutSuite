const defaultPageSize = 2
var reCount = new RegExp('_count$')

/**
 * Loads a page based on which page we want to move to
 * @param {array} pathArray         The path of where the data is stored
 * @param {number} indexDiff        Difference between current and desired page index
 */
function loadPage (pathArray, indexDiff) {
  let pageInfo = getPageInfo(pathArray)
  let pageSize = pageInfo[0]
  let pageIndex = pageInfo[1]
  pageIndex += indexDiff
  // getResourcePageSqlite being called in both statements is intentional, I want events to happen in this order to
  // prevent the user from cliking on next page multiple times and going out of bounds and I want to call loadConfig
  // to regenerate the page after Iv'e loaded SQLite data
  if (indexDiff === 0) {
    if (pathArray[2] === 'regions') {
      getResourcePageSqliteRegions(pageIndex, pageSize, pathArray[1], pathArray[3], pathArray[4])
    } else {
      getResourcePageSqlite(pageIndex, pageSize, pathArray[1], pathArray[2])
    }
  } else {
    document.getElementById('page_backward').disabled = (pageIndex <= 0)
    document.getElementById('page_forward').disabled = (pageIndex >= getLastPageIndex(pathArray, pageSize))
    if (pathArray[2] === 'regions') {
      for (let region in runResults['services'][pathArray[1]]['regions']) {
        getResourcePageSqliteRegions(pageIndex, pageSize, pathArray[1], region, pathArray[4])
      }
      loadConfig('services.' + pathArray[1] + '.regions.' + pathArray[3] + '.' + pathArray[4], 2, true)
    } else {
      getResourcePageSqlite(pageIndex, pageSize, pathArray[1], pathArray[2])
      loadConfig(pathArray[0] + '.' + pathArray[1] + '.' + pathArray[2], 2, true)
    }
  }
}

/**
 * Returns the current index of the page and it's size in number of resources
 * @param {array} pathArray         The path of where the data is stored
 * @returns {array}
 */
function getPageInfo (pathArray) {
  let pageSize, pageIndex
   if (pathArray.length === 3) {
    pageSize = runResults[pathArray[0]][pathArray[1]][pathArray[2] + '_page_size']
    pageIndex = runResults[pathArray[0]][pathArray[1]][pathArray[2] + '_page_index']
  } else if (pathArray.length === 5) {
    // Instead of following the pathArray save the data to id since that's the path of pages with regions
    if (runResults[pathArray[0]][pathArray[1]][pathArray[2]]['id'] !== undefined) {
      pageSize = runResults[pathArray[0]][pathArray[1]][pathArray[2]]['id'][pathArray[4] + '_page_size']
      pageIndex = runResults[pathArray[0]][pathArray[1]][pathArray[2]]['id'][pathArray[4] + '_page_index']
    }
  } 
  if (pageSize === undefined || pageSize === null) {
    pageSize = defaultPageSize
  }
  if (pageIndex === undefined || pageIndex === null) {
    pageIndex = 0
  }
  return [pageSize, pageIndex]
}

/**
 * Loads the first page for every resource or every resource of every region
 */
function loadFirstPageEverywhere () {
  for (let service in runResults['services']) {
    // Check if the service we are dealing with contains regions (most AWS services do)
    let regions = requestDb(createQuery('services', service, 'regions'))
    if (regions !== null && regions.keys) {
      regions = regions.keys
      // Create a 'regions' key for each service, if you know a way to not have to add in this, please fixme
      runResults['services'][service]['regions'] = {}
      for (let region in regions) {
        // Create an 'id' key for each region, this is were we will read the page index/size and load
        // the proper template
        runResults['services'][service]['regions'][regions[region]] = {id: null}
        let resources = requestDb(createQuery('services', service, 'regions', regions[region]))
        if (resources) {
          getRegionsResourcesFirstPage([regions[region]], service, resources.keys)          
        }
      }
    } else {
      for (let resource in runResults['services'][service]) {
        if (resource.match(reCount)) {
          let pathArray = ['services', service, resource.replace(reCount, '')]
          loadPage(pathArray, 0)
        }
      }
    }
  }  
}

/**
 * Loads the resources for the first page of each region in each service
 * @param {string} region           The current region we are fetching resources for 
 * @param {string} service          The current service we are fetching resources for
 * @param {object} resources        The resources we need to fetch
 */
function getRegionsResourcesFirstPage (region, service, resources) {
  for (let resource in resources) {
    // For everything that does not scale up with the ammount of resources fetch everything
    if (resources[resource] === 'id' || resources[resource] === 'region' || 
      resources[resource] === 'name' || resources[resource].match(reCount)) {
      runResults['services'][service]['regions'][region][resources[resource]] =
        requestDb(createQuery('services', service, 'regions', region, [resources[resource]]), null)
    // Else (if it scales) only fetch one page per region
    } else {
      let pathArray = ['services', service, 'regions', region, resources[resource]]
      loadPage(pathArray, 0)
    }
  }
}

/**
 * Returns the maximal index for page selection
 * @param {array} pathArray         The path of where the data is stored
 * @param {number} pageSize         The amount of resources per page
 * @returns {number}
 */
function getLastPageIndex (pathArray, pageSize) {
  let resourceCount;
  if (pathArray.length === 3) {
    resourceCount = runResults[pathArray[0]][pathArray[1]][pathArray[2] + '_count']
  } else {
    resourceCount = getHighestResourceCount(pathArray)
  }
  return Math.ceil(resourceCount / pageSize - 1)
}

/**
 * Returns the highest value of a resource count throughout regions in order to restrict pagination
 * to the proper indexes
 * @param {array} pathArray
 * @returns {number}
 */
function getHighestResourceCount (pathArray) {
  let max = 0
  for (let region in runResults[pathArray[0]][pathArray[1]][pathArray[2]]) {
    if (max < runResults[pathArray[0]][pathArray[1]][pathArray[2]][region][pathArray[4] + '_count']) {
      max = runResults[pathArray[0]][pathArray[1]][pathArray[2]][region][pathArray[4] + '_count']
    }
  }
  return max
}

/**
 * Turns off or on the pagination buttons depending on the resource page currently consulted
 */
function updateButtons () {
  let pathArray = getPathArray()
  if (pathArray.length > 1) {
    if (getFormat() === resultFormats.json) {
      hidePaginationButtons()
    } else {
      let pageInfo = getPageInfo(pathArray)
      document.getElementById('page_backward').disabled = (pageInfo[1] <= 0)
      document.getElementById('page_forward').disabled = (pageInfo[1] >= getLastPageIndex(pathArray, pageInfo[0]))
    }
  }
}

/**
 * Hides the pagination buttons
 */
function hidePaginationButtons () {
  document.getElementById('page_backward').hidden = true;
  document.getElementById('page_forward').hidden = true;
}