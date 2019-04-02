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
    loadConfig (pathArray[0] + '.' + pathArray[1] + '.' + pathArray[2], 2, true)
  }
}

/**
 * Returns the current index of the page and it's size in number of resources
 * @param {array} pathArray         The path of where the data is stored
 * @returns {array}
 */
function getPageInfo (pathArray) { 
  let pageSize, pageIndex
  pageSize = run_results[pathArray[0]][pathArray[1]][pathArray[2] + '_page_size']
  pageIndex = run_results[pathArray[0]][pathArray[1]][pathArray[2] + '_page_index']
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
  for (let service in run_results['services']) {
    for (let resource in run_results['services'][service]) {
      // Don't make a request for a page when it's a counter of resources
      if (resource.match(reCount) || resource === 'findings' || resource === 'filters') {
        continue
      }
      let pathArray = ['services', service, resource]
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
  let resourceCount = run_results[pathArray[0]][pathArray[1]][pathArray[2] + '_count']
  return Math.ceil(resourceCount / pageSize - 1)
}
