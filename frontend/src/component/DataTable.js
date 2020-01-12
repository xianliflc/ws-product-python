import React from 'react';
import MUIDataTable from 'mui-datatables';
import CustomSearchRender from './TableRenderer';
import axios from 'axios';
function updateState(text){
    console.log(text)
    this.setState({searched_rows: text})
}

class Row extends React.Component {

    state = {
        style: {'backgroundColor': '#ededed'},
        searched_rows: '',
        clear: false
    }
    
    constructor(props) {
        super(props);
        this.myRef = React.createRef()
        updateState = updateState.bind(this)
    }

    componentWillReceiveProps(newProps){
        this.setState({searched_rows: newProps.query})
    }

    shouldComponentUpdate(){
        return true
    }

    render () {
        return (
            <tr ref={this.myRef} style=
                { (this.props.query && this.props.query !== '' && this.props.poi_name.toLowerCase().toString().indexOf(this.props.query.toLowerCase()) >= 0) ? 
                    {'backgroundColor': '#ff00ff'}
                    :
                    this.state.style
                    
                }>
                <td></td>
                <td>
                    {this.props.poi_name}
                </td>
                <td>
                    {this.props.events}
                </td>
                <td>
                    {this.props.revenue}
                </td>
            </tr>
        );
    }
}

export default class TableExample extends React.Component {
    poi_url = 'http://localhost:5000/poi?include=revenue,events'
    columns = [
        {
            'name':'POI Name',
            'searchable': true,
        }, 
        {
            'name': 'No. of events',
            'searchable': false,
        },
        {
            'name': 'Revenue $',
            'searchable': false,
        }];
    options = {
        filter: true,
        selectableRows: true,
        selectableRowsHeader: false,
        filterType: 'dropdown',
        responsive: 'stacked',
        rowsPerPage: 20,
        page: 1,
        print: false,
        download: false,
        rowsPerPageOptions: [],
        caseSensitive: false,
        onTableChange: (action, tableState) => {
            // console.log(action, tableState, this.state)
        },
        customSearch: (searchQuery, currentRow, columns) => {
            this.highlightRow(searchQuery)

            return true
        },
        customSearchRender: (searchText, handleSearch, hideSearch, options) => {
            return (
                <CustomSearchRender
                    searchText={searchText}
                    onSearch={handleSearch}
                    onHide={hideSearch}
                    options={options}
                    clear={this.clearSearch.bind(this)}
                />
            );
        },
        customRowRender: data => {
            const [ poi_name, events, revenue] = data;

            return (
                <Row 
                    key={poi_name}
                    poi_name={poi_name}
                    events={events}
                    revenue={revenue}
                    query={this.state.searched_rows}
                />
            );
        }
    }

    state = {
        poi: []
    }

    clearSearch() {
        this.setState({clear: true, searched_rows: ''})
    }

    highlightRow(text) {
        this.setState({searched_rows: text, clear: false})
    }

    getData() {
        axios.get(`${this.poi_url}`)
        .then(res => {
            let poi = []
            if (res.data.data.error) {
                console.error(res.data.data.error)
            }
    
            res.data.data.forEach(item => {
                poi.push([
                    item['Poi Name'],
                    item['events'],
                    item['revenue']
                ])
            })

            this.setState({ poi: poi });
        })
    }

    componentDidMount() {
        this.getData()
    }

    render () {
        return (
            <MUIDataTable
                title={'Poi-revenue list'}
                data={this.state.poi}
                columns={this.columns}
                options={this.options} 
            />
        );
    }
}
