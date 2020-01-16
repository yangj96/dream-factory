import {Icon, Slider, Modal, Radio, List} from 'antd';
import React from 'react';
import './Box.css'
import * as config from './config'


const task_to_title = {
    fuse: 'Change Face'
}

const task_to_weight_range = {
    fuse: [0, 100],
}

const base64_head = 'data:image/png;base64,'

function getImageUrl(image_id) {
    return config.backend + 'image/' + image_id + '.png';
}

function getGanImageUrl(image_id) {
    return config.backend + 'image/gan/' + image_id + '.png';
}

function getUrl(url, params){
    if (params) {
        let paramsArray = [];
        Object.keys(params).forEach(key => paramsArray.push(key + '=' + params[key]))
        if (url.search(/\?/) === -1) {
            url += '?' + paramsArray.join('&')
        } else {
            url += '&' + paramsArray.join('&')
        }
    }
    return url
}

const idx_arr = [0, 1, 2, 3, 4, 5]
const null_res_list = [null, null, null, null, null, null]

class LargeBox extends React.Component<> {
    constructor(props) {
        super(props)
        this.state = {
            showGallery: false,
            galleryOpenFor: 1,
            image_id1: props.image_id1,
            image_id2: props.image_id2,
            chosen_id: '',
            res_list: null_res_list,
        }
        console.log(this.state.image_id, typeof(this.state.image_id), typeof(backend), config)
    }

    render() {
        return (
            <div className={'container ' + this.props.color}>
                <div className='subTopContainer'>
                <span className='title'>{task_to_title[this.props.task_type]}</span>
                </div>
                <div className='subContainer'>
                    <img src={getGanImageUrl(this.state.image_id1)}
                     onClick={() => this.setState({showGallery: true, galleryOpenFor: 1})}
                     />
                     {idx_arr.map(idx => (
                       <img src={this.state.res_list[idx]}/>
                     ))}
                    <img src={getGanImageUrl(this.state.image_id2)}
                     onClick={() => this.setState({showGallery: true, galleryOpenFor: 2})}
                     />
                </div>
                <Modal title='Gallery'
                    visible={this.state.showGallery}
                    onCancel={() => this.setState({showGallery: false})}
                    footer={null}
                >
                    <div className='modalImageContainer'>{
                        this.props.image_ids.map((image_id) =>
                        <img
                            key={image_id}
                            src={getImageUrl(image_id)}
                            onClick={() => this.setState({chosen_id: image_id})}
                            className={this.state.chosen_id == image_id ? 'chosenImage' : ''}
                            onDoubleClick={() => this.updateImage(image_id)}
                        />)
                    }</div>
                </Modal>
            </div>
        );
    }

    updateImage = (image_id) => {
        console.log(image_id)
        var image_id1 = this.state.image_id1
        var image_id2 = this.state.image_id2
        if (this.state.galleryOpenFor == 1) {
            image_id1 = image_id
        } else image_id2 = image_id
        this.setState({showGallery: false, res: null_res_list, image_id1, image_id2})
        const url = getUrl(config.backend + 'run', {
            task_type: this.props.task_type,
            image_id1: image_id1,
            image_id2: image_id2,
            resolution: config.resolution
        })
        fetch(url,{
            method: 'GET',
        })
        .then((response) => response.json())
        .then((data) => {
            var res_list = []
            for (var i = 0; i < 6; i++) {
                res_list.push(base64_head + data['images'][i])
            }
            this.setState({res_list})
        })
        .catch((error) => {
            console.error(error)
        });
    }
}

export default LargeBox
