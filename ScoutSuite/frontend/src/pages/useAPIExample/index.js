import React from 'react'
import { useAPI } from '../../api/useAPI'

export const UseAPIExample = () => {
    const { data, loading, error } = useAPI('dashboards.home')

    if (error) return <p style={{ color: 'red' }}>{error}</p>
    if (loading) return <p>Loading...</p>

    return <div>
        {Object.values(data).map((service) => {
            return <p>
                <b>Checked items:</b> {service.checked_items} <br />
                <b>Max level:</b> {service.max_level} <br />
                <b>Rules count:</b> {service.rules_count} <br />
            </p>
        })}
    </div>
}