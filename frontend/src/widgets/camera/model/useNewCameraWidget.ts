import {type ChangeEvent, type SubmitEvent, useState} from "react";
import {postCamera} from "@features/camera";
import {useNavigate} from "react-router-dom";

export const useNewCameraWidget = () => {
    const [form, setForm] = useState({
        name: '',
        model: '',
        location: '',
        rtsp: '',
    })
    const navigate = useNavigate();

    const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
        const {name, value} = e.target;
        setForm({...form, [name]: value});
    }

    const onSubmitCameraForm = (e:SubmitEvent<HTMLFormElement>) => {
        e.preventDefault()

        try{
            postCamera(form)
            alert(`${form.name} 등록 되었습니다.`);
            navigate('/cameras')
        }catch (e) {
            console.error('등록 실패', e)
        }
    }

    return {form, handleChange, onSubmitCameraForm};
}