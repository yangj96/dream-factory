import {Icon, Slider, Modal, Radio} from 'antd';
import React from 'react';
import './Box.css'
import * as config from './config'

const hair_colors= config.hair_colors
const emotions = config.emotions

const task_to_title = {
    fuse: 'Change Face',
    gender: 'Change Gender',
    age: 'Change Age',
    makeup: 'Makeup (Removal)',
    hair: 'Change Hair Color',
    emotion: 'Change Emotion',
    glasses: 'Wear Glasses',
    head_yaw: 'Yaw Head',
    facial_hair: 'Change Mustache',
    exposure: 'Whitening',
    smile: 'Change Smile'
};

const task_to_weight_range = {
    fuse: [0, 100],
    gender: [-50, 50],
    age: [-50, 50],
    makeup: [-50, 50],
    hair: [0, 100],
    emotion: [0, 100],
    glasses: [-50, 50],
    head_yaw: [-50, 50],
    facial_hair: [-50, 50],
    exposure: [-50, 50],
    smile: [-50, 50]
};

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

class Box extends React.Component<> {
    constructor(props) {
        super(props)
        var choice = null
        if (props.task_type == 'hair') choice = hair_colors[0]
        if (props.task_type == 'emotion') choice = emotions[0]
        this.state = {
            showGallery: false,
            image_id: props.image_id,
            slider: true,
            chosen_id: '',
            weight: 0,
            res: null,
            choice
        }
        console.log(this.state.image_id, typeof(this.state.image_id), typeof(backend), config)
    }

    render() {
        return (
            <div className={'container ' + this.props.color}>
                <div className='subTopContainer'>
                <span className='title'>{task_to_title[this.props.task_type]}</span>
                {this.props.task_type == 'hair' && (
                    <Radio.Group
                        defaultValue={hair_colors[0]}
                        onChange={(e) => this.setState({choice: e.target.value})}>
                        {hair_colors.map(color => (
                        <Radio.Button value={color}>{color}</Radio.Button>
                        ))}
                   </Radio.Group>
                )}
                 {this.props.task_type == 'emotion' && (
                    <Radio.Group
                        defaultValue={emotions[0]}
                        onChange={(e) => this.setState({choice: e.target.value})}>
                        {emotions.map(emotion => (
                        <Radio.Button value={emotion}>{emotion}</Radio.Button>
                        ))}
                   </Radio.Group>
                )}
                </div>
                <div className='subContainer'>
                    <img src={getGanImageUrl(this.state.image_id)}
                     onClick={() => this.setState({showGallery: true})}
                     />
                    <div class='invisibleImageContainer'><img src={this.state.res}/></div>
                    {this.state.slider &&
                    (<div className='sliderContainer'>
                    <Slider vertical
                        defaultValue={0}
                        min={task_to_weight_range[this.props.task_type][0]}
                        max={task_to_weight_range[this.props.task_type][1]}
                        onAfterChange={this.submit}
                        />
                    </div>)
                    }
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
                            onDoubleClick={() => this.setState({showGallery: false, res: null, image_id})}
                        />)
                    }</div>
                </Modal>
            </div>
        );
    }

    submit = (weight) => {
        console.log('gogogo')
        
        switch(this.props.task_type) {
            case 'age':
                weight /= 40
                break
            case 'gender':
                weight /= 15
                break
            case 'makeup':
                weight /= 10
                break
            case 'facial_hair':
                weight /= 15
                break
            case 'exposure':
                weight /= 5
                break
            case 'smile':
                weight /= 50
                break
            case 'head_yaw':
                weight /= 30
                break
            case 'hair':
                weight = this.state.choice == 'brown' ? weight / 20 : weight / 50
                break
            case 'emotion':
                if (this.state.choice == 'sad')
                    weight /= 25
                else weight /= 30
                break
            default:
                weight /= 25
        }

        const url = getUrl(config.backend + 'run', {
            weight: weight,
            task_type: this.props.task_type,
            image_id1: this.state.image_id,
            choice: this.state.choice
        });
        fetch(url,{
            method: 'GET',
        })
        .then((response) => response.json())
        .then((data) => {
            this.setState({'res': base64_head + data['images'][0]})
        })
        .catch((error) => {
            console.error(error)
        });
    }
}

export default Box
