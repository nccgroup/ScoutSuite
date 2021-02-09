import { useEffect, useState } from 'react'
import * as API from './api'

/**
 * React Hook to fetch API data and re-render the component
 * @param {*} path
 */
export const useAPI = (path) => {
    const [data, setData] = useState({})
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    useEffect(() => {
        const asyncAPI = async () => {
            setLoading(true)
            try {
                const response = await API.get(path)
                setData(response)
            } catch(e) {
                setError('Oops! Something went wrong loading this content. Is the server working?')
                console.error(e.message)
            }
            setLoading(false)
        }
        asyncAPI()
    }, [path])

    const loadMore = () => {
    // TODO: Load more content when the content is paginated
    }

    return {data, loading, error, loadMore}
}
