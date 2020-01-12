import React, { PureComponent } from 'react';
import {
  ComposedChart, Line, Area, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  Legend,
} from 'recharts';
import axios from 'axios';
import {DateDifference} from '../utils/DateUtils'

export default class Example extends PureComponent {
    default_start_date = '2017-01-01'
    default_end_date = '2017-01-07'
    stats_daily_url = 'http://localhost:5000/stats/daily'
    stats_hourly_url = 'http://localhost:5000/stats/hourly'
    filter_type = 'daily'

	constructor(props) {
        super(props);
        this.myRef = React.createRef();
        this.myRef2 = React.createRef();
        this.filter_type_ref = React.createRef();
        this.changeDate = this.changeDate.bind(this)
        this.changeType = this.changeType.bind(this)
	}

    state = {
        stats: [],
    }

    getData(start_date, end_date) {
        const day_difference = DateDifference(start_date, end_date) + 1
        if (day_difference > 7) {
            alert('Range should be maximum of 7 days')
            return
        }
        const base_url = this.filter_type === 'daily' ? this.stats_daily_url : this.stats_hourly_url
        axios.get(`${base_url}?start_date=${start_date}&end_date=${end_date}`)
            .then(res => {
                if (res.data.data.error) {
                    console.error(res.data.data.error)
                }
                res.data.data.forEach(item => {
                    item.impressions = Math.round(item.impressions / 100)
                    item.revenue = Math.round(item.revenue)
                })

            const stats = res.data.data;
            this.setState({ stats });
            
        })
    }

    componentDidMount() {
        this.getData(this.default_start_date, this.default_end_date, this.filter_type)
    }

    changeDate(e) {
        e.preventDefault()
        console.log(this.filter_type_ref, this.filter_type_ref.current.f)
        this.getData(this.myRef.current.value, this.myRef2.current.value)
    }

    changeType(e) {
        this.filter_type = e.target.value
    }

  render() {
    return (
        <div>
            <form onSubmit={this.changeDate}>
                <div>
                    <input type="date" ref={this.myRef} />
                    <input type="date" ref={this.myRef2} />
                </div>
                <div ref={this.filter_type_ref} onChange={this.changeType}>
                    <input type="radio" name="type" value="daily" /> daily
                    <input type="radio" name="type" value="hourly" /> hourly
                </div>
                <button type="submit"> Submit </button>
            </form>
            <ComposedChart
                width={1000}
                height={900}
                data={this.state.stats}
                margin={{
                top: 50, right: 80, bottom: 25, left: 50,
                }}
            >
                <CartesianGrid stroke="#f5f5f5" />
                <XAxis dataKey={this.filter_type === 'daily'? 'date' : 'hour'}
                label={{ value: this.filter_type === 'daily'? 'Day' : 'Hour', position: 'insideBottomRight', offset: 0 }} />
                <YAxis label={{ value: 'impressions (x100)', angle: -90, position: 'insideTopLeft' }} />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="impressions" stroke="#8884d8" />
                <Line dataKey="clicks" barSize={20} stroke="#413ea0" />
                <Line type="monotone" dataKey="revenue" stroke="#ff7300" />
            </ComposedChart>
        </div>
    );
  }
}
