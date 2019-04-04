var defaultPageSize = 2
var reCount = new RegExp('_count+$')

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
    if (pathArray.length === 3) {
      getResourcePageSqlite(pageIndex, pageSize, pathArray[1], pathArray[2])
    } else if (pathArray.length === 5) {
      // Need to iterate through the regions here or else it will try to get some data at regions.id because that
      // is the path of the resource in the URI
      for (let region in runResults[pathArray[0]][pathArray[1]][pathArray[2]]) {
        getResourcePageSqliteRegions(pageIndex, pageSize, pathArray[1], region, pathArray[4])
      }
    }
  } else {
    document.getElementById('page_backward').disabled = (pageIndex <= 0)
    document.getElementById('page_forward').disabled = (pageIndex >= getLastPageIndex(pathArray, pageSize))
    if (pathArray.length === 3) {
      getResourcePageSqlite(pageIndex, pageSize, pathArray[1], pathArray[2])
      loadConfig(pathArray[0] + '.' + pathArray[1] + '.' + pathArray[2], 2, true)
    } else if (pathArray.length === 5) {
      for (let region in runResults[pathArray[0]][pathArray[1]][pathArray[2]]) {
        getResourcePageSqliteRegions(pageIndex, pageSize, pathArray[1], region, pathArray[4])
      }
      loadConfig(pathArray[0] + '.' + pathArray[1] + '.' + pathArray[2] + '.' + pathArray[3] + '.' + pathArray[4], 
        2, true)
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
    pageSize = runResults[pathArray[0]][pathArray[1]][pathArray[2]][pathArray[3]][pathArray[4] + '_page_size']
    pageIndex = runResults[pathArray[0]][pathArray[1]][pathArray[2]][pathArray[3]][pathArray[4] + '_page_index']
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
 * Loads the first page for every resource
 */
function loadFirstPageEverywhere () {
  for (let service in runResults['services']) {
    if (runResults['services'][service]['regions']) {
      // If there is not already a propriety for regions.id we need to create one since the regions resources
      // are viewable under that path and we read the path to know what to show to the user
      if (!runResults['services'][service]['regions']['id']) {
        runResults['services'][service]['regions']['id'] = null
      }
      for (let region in runResults['services'][service]['regions']) {
        for (let resource in runResults['services'][service]['regions'][region]) {
          if (resource.match(reCount)) {
            let pathArray = ['services', service, 'regions', region, resource.replace(reCount, '')]
            loadPage(pathArray, 0)
          }
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
 * Returns the maximal index for page selection
 * @param {array} pathArray         The path of where the data is stored
 * @param {number} pageSize         The amount of resources per page
 * @returns {number}
 */
function getLastPageIndex (pathArray, pageSize) {
  let resourceCount = 1
  if (pathArray.length === 3) {
    resourceCount = runResults[pathArray[0]][pathArray[1]][pathArray[2] + '_count']
  } else {
    resourceCount = runResults[pathArray[0]][pathArray[1]][pathArray[2]][pathArray[3]][pathArray[4] + '_count']
  }
  return Math.ceil(resourceCount / pageSize - 1)
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