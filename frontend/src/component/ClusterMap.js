import axios from 'axios'
import React from 'react'
const { compose, withProps, withHandlers } = require("recompose")
const {
    withScriptjs,
    withGoogleMap,
    GoogleMap,
    Marker,
} = require("react-google-maps")
const { MarkerClusterer } = require("react-google-maps/lib/components/addons/MarkerClusterer")

const MapWithAMarkerClusterer = compose(
    withProps({
        googleMapURL: "https://maps.googleapis.com/maps/api/js?key=AIzaSyAnKu85VSoJJASFOAP2K-sgQbsu6Hm9PoU&v=3.exp&libraries=geometry,drawing,places",
        loadingElement: <div style={{ height: `100%` }} />,
        containerElement: <div style={{ height: `400px` }} />,
        mapElement: <div style={{ height: `100%` }} />,
    }),
    withHandlers({
        onMarkerClustererClick: () => (markerClusterer) => {
            // const clickedMarkers = markerClusterer.getMarkers()
        },
    }),
    withScriptjs,
    withGoogleMap
)(props =>
    <GoogleMap
        defaultZoom={4}
        defaultCenter={{ lat: 43, lng: -79 }}
    >
        <MarkerClusterer
        onClick={props.onMarkerClustererClick}
        averageCenter
        enableRetinaIcons
        gridSize={60}
        >
            {props.markers.map(marker => (
                <Marker
                key={marker.poi_id}
                position={{ lat: marker.lat, lng: marker.lon }}
                />
            ))}
        </MarkerClusterer>
    </GoogleMap>
)

export default class ClusterMap extends React.PureComponent {
    poi_url = 'http://localhost:5000/poi?include=revenue,events'
    default_min_revenue = 0
    default_max_revenue = 1000000000
    default_min_events = 0
    default_max_events = 1000000000

    constructor(props) {
        super(props);
        this.max_revenue_ref = React.createRef();
        this.min_revenue_ref = React.createRef();
        this.max_events_ref = React.createRef();
        this.min_events_ref = React.createRef();
        this.filterServer = this.filterServer.bind(this)

    }
    
    componentWillMount() {
        this.setState({ markers: [] })
    }

    componentDidMount() {
        this.getData(
            this.default_min_revenue,
            this.default_max_revenue,
            this.default_min_events,
            this.default_max_events
        )
    }

    getData(min_revenue, max_revenue, min_events, max_events) {
        axios.get(`${this.poi_url}&min_revenue=${min_revenue}&max_revenue=${max_revenue}&min_events=${min_events}&max_events=${max_events}`)
        .then(res => {
            if (res.data.data.error) {
                alert(JSON.stringify(res.data.data.error))
                console.error(res.data.data.error )
            }
            this.setState({ markers: res.data.data })
        })
    }

    filterServer(e) {
        e.preventDefault()
        this.getData(
 
            isNaN(parseInt(this.min_revenue_ref.current.value)) ? this.default_min_revenue : parseInt(this.min_revenue_ref.current.value),
            isNaN(parseInt(this.max_revenue_ref.current.value))? this.default_max_revenue : parseInt(this.max_revenue_ref.current.value),
            isNaN(parseInt(this.min_events_ref.current.value)) ? this.default_min_events : parseInt(this.min_events_ref.current.value),
            isNaN(parseInt(this.max_events_ref.current.value)) ? this.default_max_events: parseInt(this.max_events_ref.current.value)
        )
    }

    render() {
        return (
            <div>
                <form onSubmit={this.filterServer}>
                    Min revenue <input type="text" ref={this.min_revenue_ref} />
                    Max revenue <input type="text" ref={this.max_revenue_ref} />
                    Min events <input type="text" ref={this.min_events_ref} />
                    Max events <input type="text" ref={this.max_events_ref} />
                    <button type="submit"> Submit </button>
                </form>
                <MapWithAMarkerClusterer markers={this.state.markers} />
            </div>
        )
    }
}