import React from 'react';
import Grow from '@material-ui/core/Grow';
import TextField from '@material-ui/core/TextField';
import IconButton from '@material-ui/core/IconButton';
import ClearIcon from '@material-ui/icons/Clear';
import { withStyles } from '@material-ui/core/styles';

const defaultSearchStyles = theme => ({
    main: {
        display: 'flex',
        flex: '1 0 auto',
    },
    searchText: {
        flex: '0.8 0',
    },
    clearIcon: {
        '&:hover': {
            color: theme.palette.error.main,
        },
    },
});

class CustomSearchRender extends React.Component {
    handleTextChange = event => {
        // console.log(event.target, event.target.value)
        this.props.onSearch(event.target.value);
    };

    componentDidMount() {
        document.addEventListener('keydown', this.onKeyDown, false);
    }

    componentWillUnmount() {
        document.removeEventListener('keydown', this.onKeyDown, false);
    }

    onKeyDown = event => {
        if (event.keyCode === 27) {
            this.props.onHide();
        }
    };

    onKeyUp = event => {

        if (event.keyCode === 8 && event.target.value === '') {
            this.handleTextChange(event)
            this.props.clear()
        }
    };

    render() {
        const { classes, options, onHide, searchText } = this.props;

        return (
        <Grow appear in={true} timeout={300}>
            <div className={classes.main} ref={el => (this.rootRef = el)}>
            <TextField
                placeholder={'Search...'}
                className={classes.searchText}
                InputProps={{
                    'aria-label': options.textLabels.toolbar.search,
                }}
                value={searchText || ''}
                onChange={this.handleTextChange}
                onKeyUp={this.onKeyUp}
                fullWidth={true}
                inputRef={el => (this.searchField = el)}
            />
            <IconButton className={classes.clearIcon} onClick={onHide}>
                <ClearIcon />
            </IconButton>
            </div>
        </Grow>
        );
    }
}

export default withStyles(defaultSearchStyles, { name: 'CustomSearchRender' })(CustomSearchRender);