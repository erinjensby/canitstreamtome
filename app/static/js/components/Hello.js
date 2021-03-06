import React from 'react';

export class ModelGrid extends React.Component {
		constructor(props) {
		super(props);
	}

	render() {
		const movieList = this.props.info;

		return (
			<section>
			<div className="container">
			<div className="row align-items-center">
				{movieList.map(function(value){
					return <ModelItem src={`/static/img/${value}`} alt="" />
				})}
			</div>
			</div>
			</section>
		);

	}
}

export class ModelItem extends React.Component {
		constructor(props) {
		super(props);
	}

	render() {
		return (
			<div className="col-sm-3">
				<a href={this.props.ref}>
					<img className="img-responsive" src={this.props.src} alt={this.props.alt} />
				</a>
			</div>
		);
	}
}

