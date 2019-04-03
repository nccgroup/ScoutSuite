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
    getResourcePageSqlite(pageIndex, pageSize, pathArray[1], pathArray[2])
  } else {
    document.getElementById('page_backward').disabled = (pageIndex <= 0)
    document.getElementById('page_forward').disabled = (pageIndex >= getLastPageIndex(pathArray, pageSize))
    getResourcePageSqlite(pageIndex, pageSize, pathArray[1], pathArray[2])    
    loadConfig(pathArray[0] + '.' + pathArray[1] + '.' + pathArray[2], 2, true)
  }
}

/**
 * Returns the current index of the page and it's size in number of resources
 * @param {array} pathArray         The path of where the data is stored
 * @returns {array}
 */
function getPageInfo (pathArray) { 
  let pageSize, pageIndex
  pageSize = runResults[pathArray[0]][pathArray[1]][pathArray[2] + '_page_size']
  pageIndex = runResults[pathArray[0]][pathArray[1]][pathArray[2] + '_page_index']
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
    for (let resource in runResults['services'][service]) {
      // Don't make a request for a page when it's a counter of resources
      if (resource.match(reCount)) {
        let pathArray = ['services', service, resource.replace(reCount, '')]
        loadPage(pathArray, 0)
        continue
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
  let resourceCount = runResults[pathArray[0]][pathArray[1]][pathArray[2] + '_count']
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