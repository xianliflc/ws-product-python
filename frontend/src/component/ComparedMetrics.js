import React, { PureComponent } from 'react';
import {
  ComposedChart, Line, Area, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  Legend,
} from 'recharts';
import axios from 'axios';
import {DateDifference} from '../utils/DateUtils'

export default class Example extends PureComponent {
    default_start_date = '2017-01-01'
    default_end_date = '2017-01-03'
    default_start_date2 = '2017-01-04'
    default_end_date2 = '2017-01-06'
    stats_daily_url = 'http://localhost:5000/stats/daily'
    stats_hourly_url = 'http://localhost:5000/stats/hourly'
    filter_type = 'daily'
    metrics = 'revenue'

	constructor(props) {
        super(props);
        this.start_date_ref = React.createRef();
        this.end_date_ref = React.createRef();
        this.start_date_ref2 = React.createRef();
        this.end_date_ref2 = React.createRef();
        this.filter_type_ref = React.createRef();
        this.metrics_ref = React.createRef();
        this.changeDate = this.changeDate.bind(this)
        this.changeType = this.changeType.bind(this)
        this.changeMetrics = this.changeMetrics.bind(this)
	}

    state = {
        stats: [],
    }

    getData(start_date, end_date, start_date2, end_date2) {
        const day_difference = DateDifference(start_date, end_date) + 1
        if (day_difference > 5) {
            alert('Range should be maximum of 5 days')
            return
        }

        const day_difference2 = DateDifference(start_date2, end_date2) + 1
        if (day_difference2 > 5) {
            alert('Compared date range should be maximum of 5 days')
            return
        }

        if (day_difference !== day_difference2) {
            alert('Compared date ranges do not have the same length')
            return
        }
        const base_url = this.filter_type === 'daily' ? this.stats_daily_url : this.stats_hourly_url
        const req1 = axios.get(`${base_url}?start_date=${start_date}&end_date=${end_date}`)
        const req2 = axios.get(`${base_url}?start_date=${start_date2}&end_date=${end_date2}`)
        axios.all([req1, req2]) 
        .then(axios.spread((...responses) => {

            if (responses[0].data.data.error) {
                console.error(responses[0].data.data.error)
            }

            if (responses[1].data.data.error) {
                console.error(responses[1].data.data.error)
            }
            responses[0].data.data.forEach(item => {
                item.impressions = Math.round(item.impressions / 1000)
                item.revenue = Math.round(item.revenue)
            })

            let stats = responses[0].data.data;

            responses[1].data.data.forEach((item, index) => {
                stats[index]['impressions2'] = Math.round(item.impressions / 1000)
                stats[index]['revenue2'] = Math.round(item.revenue)
                stats[index]['clicks2'] = item.clicks
            })
            
            this.setState({ stats})
            
        }))
    }

    componentDidMount() {
        this.getData(
            this.default_start_date,
            this.default_end_date,
            this.default_start_date2,
            this.default_end_date2
        )
    }

    changeDate(e) {
        e.preventDefault()
        console.log(this.filter_type_ref, this.filter_type_ref.current.f)
        this.getData(
            this.start_date_ref.current.value,
            this.end_date_ref.current.value,
            this.start_date_ref2.current.value,
            this.end_date_ref2.current.value
        )
    }

    changeType(e) {
        this.filter_type = e.target.value
    }

    changeMetrics(e) {
        this.metrics = e.target.value
    }

  render() {
    return (
        <div>
            <form onSubmit={this.changeDate}>
                <div>
                    <input type="date" ref={this.start_date_ref} />
                    <input type="date" ref={this.end_date_ref} /> 
                </div>
                compared to 
                <div>
                    <input type="date" ref={this.start_date_ref2} />
                    <input type="date" ref={this.end_date_ref2} />
                </div>
                <div ref={this.metrics_ref} onChange={this.changeMetrics}>
                    <input type="radio" name="metrics" value="clicks" /> clicks
                    <input type="radio" name="metrics" value="impressions" /> impressions
                    <input type="radio" name="metrics" value="revenue" /> revenue
                </div>
                <div ref={this.filter_type_ref} onChange={this.changeType}>
                    <input type="radio" name="type" value="daily" /> daily
                    <input type="radio" name="type" value="hourly" /> hourly
                </div>
                <button type="submit"> Submit </button>
            </form>
            <ComposedChart
                width={1200}
                height={1000}
                data={this.state.stats}
                margin={{
                top: 50, right: 80, bottom: 25, left: 50,
                }}
            >
                <CartesianGrid stroke="#f5f5f5" />
                <XAxis dataKey={this.filter_type === 'daily'? 'date' : 'hour'}
                    label={{ value: this.filter_type === 'daily'? 'Day' : 'Hour', position: 'insideBottomRight', offset: 0 }} />
                <YAxis label={{ value: this.metrics, angle: -90, position: 'insideTopLeft' }} />
                <Tooltip />
                <Legend />
                <Bar dataKey={this.metrics} barSize={12} fill="#413ea0" />
                <Bar dataKey={this.metrics + '2'} barSize={12} fill="#ff7300" />
            </ComposedChart>
        </div>
    );
  }
}
