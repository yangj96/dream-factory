import { Layout, Breadcrumb, Card, Col, Row, Collapse } from 'antd';
import React from 'react';
import './App.css'
import Box from './Box'
import LargeBox from './LargeBox'
import * as config from './config'

const { Header, Content, Footer } = Layout
const { Panel } = Collapse

class App extends React.Component<> {
  constructor() {
    super()
    this.state = {
      image_names: null,
      image_ids: null,
      init_image_id: null
    }
  }
  render() {
    if(!this.state.init_image_id) return null;

    return (
      <Layout className="layout">
        <Header>
          <div className="logo">
            <span>Dream Factory - Image Semantic Editing</span>
          </div>
        </Header>
        <div className='boxContainer'>
          <LargeBox task_type='fuse' color='blue' image_id1='67138' image_id2='67139' image_ids={this.state.image_ids} image_names={this.state.image_names}/>

          <Box task_type='makeup' color='yellow' image_id={this.state.init_image_id} image_ids={this.state.image_ids} image_names={this.state.image_names}/>
          <Box task_type='glasses' color='green' image_id={this.state.init_image_id} image_ids={this.state.image_ids} image_names={this.state.image_names}/>

          <Box task_type='hair' color='red' image_id={this.state.init_image_id} image_ids={this.state.image_ids} image_names={this.state.image_names}/>
          <Box task_type='emotion' color='blue' image_id={this.state.init_image_id} image_ids={this.state.image_ids} image_names={this.state.image_names}/>
          
          <Box task_type='age' color='green' image_id={this.state.init_image_id} image_ids={this.state.image_ids} image_names={this.state.image_names}/>
          <Box task_type='gender' color='yellow' image_id={this.state.init_image_id} image_ids={this.state.image_ids} image_names={this.state.image_names}/>
      
          <Box task_type='facial_hair' color='red' image_id={this.state.init_image_id} image_ids={this.state.image_ids} image_names={this.state.image_names}/>
          <Box task_type='exposure' color='blue' image_id={this.state.init_image_id} image_ids={this.state.image_ids} image_names={this.state.image_names}/>
          <Box task_type='smile' color='green' image_id={this.state.init_image_id} image_ids={this.state.image_ids} image_names={this.state.image_names}/>
          <Box task_type='head_yaw' color='yellow' image_id={this.state.init_image_id} image_ids={this.state.image_ids} image_names={this.state.image_names}/>
          
         
        </div>
        <Footer style={{textAlign: 'center'}}>
          Dream Factory ©2020 Created by Google Winter ML Camp X.Y.Z Team
        </Footer>
      </Layout>
    );
  }

  componentWillMount() {
      fetch(config.backend + 'imagenames', {
        method: 'GET',
      })
        .then((response) => response.json())
        .then((data) => {
          this.setState({
            ...data,
            init_image_id: data['image_ids'].indexOf('67138') == -1 ? data['image_ids'][0] : '67138'
          })
          console.log(this.state)
        })
        .catch((error) => {
            alert(error)
        });
  }
}

export default App;