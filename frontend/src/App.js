import React from "react";
import ReactDOM from "react-dom";
import GlobalSearchComponent from "./GlobalSearchComponent";
import ReactTable from "react-table";
import "react-table/react-table.css";
import "./styles.css";

const API_URL = process.env.REACT_APP_API_URL;
if (!API_URL) {
  console.warn("API_URL is undefined");
}

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      filteredData: [],
      columns: [],
      searchInput: ""
    };
  }

  async componentDidMount() {
    await this.getColumns();
    this.getData();
  }

  async getColumns() {
    if (!API_URL) {
      throw new Error("API_URL is undefined");
    }
    const res = await fetch(`${API_URL}/courses`);
    const courseList = await res.json();
    console.log(courseList);

    var columns_ = [];
    columns_.push({
      Header: "Имя",
      accessor: "name",
      sortable: true,
      show: true,
      displayValue: "Имя"
    });

    for (var i = 0; i < courseList.length; i++)
    {
      columns_.push({
        Header: courseList[i].name,
        accessor: courseList[i].id.toString(),
        sortable: true,
        show: true,
        displayValue: courseList[i].name,
      });
    }

    // let columns = [
    //   {
    //     Header: "First Name",
    //     accessor: "firstName",
    //     sortable: false,
    //     show: true,
    //     displayValue: " First Name"
    //   },
    //   {
    //     Header: "Status",
    //     accessor: "status",
    //     sortable: false,
    //     show: true,
    //     displayValue: "Status "
    //   },
    //   {
    //     Header: "Visits",
    //     accessor: "visits",
    //     sortable: false,
    //     show: true,
    //     displayValue: " Visits "
    //   }
    // ];
    let columns = columns_;
    this.setState({ columns });
  }

  async getData() {
    if (!API_URL) {
      throw new Error("API_URL is undefined");
    }
    const res = await fetch(`${API_URL}/users`);
    const userList = await res.json();
    // const res2 = await fetch(`${API_URL}/applications`);
    // const applicList = await res.json();
    console.log(userList);

    var data_ = [];
    for (var i = 0; i < userList.length; i++)
    {
      const user = {};
      user.name = userList[i].name + " " + userList[i].surname;
      for (var j = 1; j < this.state.columns.length; j++)
      {
        user[this.state.columns[j].accessor] = "+";
      }
      console.log(user);
      data_.push(user);
      // columns_.push({
      //   Header: courseList[i].name,
      //   accessor: courseList[i].id,
      //   sortable: true,
      //   show: true,
      //   displayValue: courseList[i].name,
      // });
    }
    console.log(data_);

    // let data = [
    //   { firstName: "aaaaa", status: "Pending", visits: 155 },
    //   { firstName: "aabFaa", status: "Pending", visits: 155 },
    //   { firstName: "adaAAaaa", status: "Approved", visits: 1785 },
    //   { firstName: "aAaaaa", status: "Approved", visits: 175 },
    //   { firstName: "adaSaaa", status: "Cancelled", visits: 165 },
    //   { firstName: "aasaaa", status: "Cancelled", visits: 157 },
    //   { firstName: "aweaaaaaewea", status: "Approved", visits: 153 },
    //   { firstName: "adaAAadsdweaa", status: "Approved", visits: 17585 },
    //   { firstName: "aAaaaa", status: "Approved", visits: 175 },
    //   { firstName: "adadsdSaaa", status: "Cancelled", visits: 165 },
    //   { firstName: "dsdcdaaaaa", status: "Cancelled", visits: 157 },
    //   { firstName: "aaadvsaa", status: "Submitted", visits: 5153 },
    //   { firstName: "aaaaswea", status: "Pending", visits: 1555 },
    //   { firstName: "aaaaauwe", status: "Submitted", visits: 155 }
    // ];
    let data = data_;
    this.setState({ data, filteredData: data });
  }

  handleSetData = data => {
    console.log(data);
    this.setState({ filteredData: data });
  };

  render() {
    let { filteredData, columns } = this.state;
    return (
      <div>
        <GlobalSearchComponent
          data={this.state.data}
          handleSetData={this.handleSetData}
        />
        <ReactTable
          data={filteredData}
          columns={columns}
          defaultPageSize={10}
          className="-striped -highlight"
        />
      </div>
    );
  }
}
