import React from "react";
import { Input } from "semantic-ui-react";

export default class DropDownComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      searchInput: ""
    };
  }

  handleChange = (event) => {
    this.setState({ searchInput: event.target.value }, () =>
      this.globalSearch()
    );
  };

  globalSearch = () => {
    let { searchInput } = this.state;
    let filteredData = this.props.data.filter((value) => {
      return (
        value.firstName.toLowerCase().includes(searchInput.toLowerCase()) ||
        value.status.toLowerCase().includes(searchInput.toLowerCase()) ||
        value.visits
          .toString()
          .toLowerCase()
          .includes(searchInput.toLowerCase())
      );
    });
    this.props.handleSetData(filteredData);
  };

  render() {
    return (
      <>
        <br />
        <Input
          size="large"
          name="searchInput"
          value={this.state.searchInput || ""}
          onChange={this.handleChange}
          label="Search"
        />
        <br />
        <br />
      </>
    );
  }
}
