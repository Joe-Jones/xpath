/** @jsx React.DOM */

var ResultItem = React.createClass({
	render: function() {
		return (
			<div className="resultItem">
				<pre dangerouslySetInnerHTML={ {__html: this.props.content} } />
			</div>
		);
	}
});

var ResultSet = React.createClass({
	render: function() {
		var results = this.props.result_set.map(function(result) {
			return ( <ResultItem content={result} /> )
		});
		return (
			<div className="resultList">
				{results}
			</div>
		);
	}
});

var UI = React.createClass({
	getInitialState: function() {
		return {result_set: [], path: "/", valid: "T"};
	},
	loadResultSetFromServer: function() {
		$.ajax({
			url: "/run/" + sessionkey,
			dataType: 'json',
			success: function(data) {
				this.setState({result_set: data, path: this.state.path, valid: this.state.valid});
			}.bind(this),
			error: function(xhr, status, err) {
				console.error(this.props.url, status, err.toString());
			}.bind(this)
		});
	},
	componentDidMount: function() {
		this.loadResultSetFromServer();
		setInterval(this.compile, 3000);
	},
	compile: function() {
		var path = this.refs.path.getDOMNode().value.trim();
		this.setState({result_set: this.state.result_set, path: path, valid: this.state.valid});
		if (path != this.state.path) {
			$.ajax({
				type: "POST",
				url: "/compile/" + sessionkey,
				dataType: 'text',
				data: {path: path},
				success: function(data) {
					console.log(data);
					this.setState({result_set: this.state.result_set, path: this.state.path, valid: data});
				}.bind(this),
				error: function(xhr, status, err) {
					console.log("wert");
					this.setState({result_set: this.state.result_set, path: this.state.path, valid: "F"});
					//console.error(this.props.url, status, err.toString());
				}.bind(this)
			});
		}
	},
	render: function() {
		var style;
		switch(this.state.valid) {
			case "T": style = {background: "#7cfc00"}; break;
			case "F": style = {background: "#ff0000"}; break;
			case "": style = {background: "#fffff0"}; break;
		}
		style["width"] = "100";
		return (
			<div>
				Type an xpath expression into the box, it will turn red if the expression can't be compiled and green again when it can.
				Pressing the button will run the compiled expression on the document below. Here are some examples you can try<br/>
				//book[@id="bk102"]<br/>
				//book[contains(description,"Oberon")]<br/>
				//book[@id="bk101"]/price/text()+//book[@id="bk104"]/price/text()<br/>
				<input type="text" value={this.state.path} ref="path" onChange={this.compile} style={style} />
				<button onClick={this.loadResultSetFromServer}>Query</button>
				<br/>
				<ResultSet result_set={this.state.result_set} />
			</div>
		);
	}	
})
      
React.renderComponent(
  <UI/>,
  document.getElementById('content')
);

