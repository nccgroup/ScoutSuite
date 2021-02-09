/**
 * Local cache for the API
 * When using this librairy, use `import * as Cache from "./cache"`
 */

let cache = new Map()

/**
 * Check if the cache contain an element
 * @param {*} path
 */
export const has = (path) => {
    return cache.has(path)
}

/**
 * Set a cache element
 * @param {*} path
 * @param {*} data
 */
export const set = (path, data) => {
    return cache.set(path, data)
}

/**
 * Get a element from the cache
 * @param {*} path
 */
export const get = (path) => {
    return cache.get(path)
}

/**
 * Remove an element from the cache
 * @param {*} path
 */
export const remove = (path) => {
    cache.delete(path)
}
