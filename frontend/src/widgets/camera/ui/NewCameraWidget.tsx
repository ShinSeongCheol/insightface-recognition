import {useNewCameraWidget} from "@/widgets/camera/model/useNewCameraWidget.ts";
import {AddCameraButton, CancelCameraButton} from "@features/camera";

export const NewCameraWidget = () => {
    const {form, handleChange, onSubmitCameraForm} = useNewCameraWidget()

    return (
        <div className={'min-h-screen flex justify-center items-center'}>
            <form className={'bg-white w-xl p-8 rounded-xl shadow-xl border border-gray-100 grid grid-cols-[80px_auto_1fr] gap-4 text-left items-center'} onSubmit={onSubmitCameraForm}>
                <label className={'text-sm font-bold text-gray-600 ml-1'}>이름</label>
                <span className={'text-gray-400 text-center'}>:</span>
                <input type="text" name={'name'} className={'bg-gray-100 p-2 px-3 border-none rounded-md focus:ring-2 focus:ring-blue-500 text-md font-medium outline-none transition-all'} value={form.name} onChange={handleChange}/>

                <label className={'text-sm font-bold text-gray-600 ml-1'}>모델명</label>
                <span className={'text-gray-400 text-center'}>:</span>
                <input type="text" name={'model'} className={'bg-gray-100 p-2 px-3 border-none rounded-md focus:ring-2 focus:ring-blue-500 text-md font-medium outline-none transition-all'} value={form.model} onChange={handleChange}/>

                <label className={'text-sm font-bold text-gray-600 ml-1'}>설치위치</label>
                <span className={'text-gray-400 text-center'}>:</span>
                <input type="text" name={'location'} className={'bg-gray-100 p-2 px-3 border-none rounded-md focus:ring-2 focus:ring-blue-500 text-md font-medium outline-none transition-all'} value={form.location} onChange={handleChange}/>

                <label className={'text-sm font-bold text-gray-600 ml-1'}>RTSP 주소</label>
                <span className={'text-gray-400 text-center'}>:</span>
                <input type="text" name={'rtsp'} className={'bg-gray-100 p-2 px-3 border-none rounded-md focus:ring-2 focus:ring-blue-500 text-md font-medium outline-none transition-all'} value={form.rtsp} onChange={handleChange}/>

                <div className={'col-span-3 mt-4 flex gap-4'}>
                    <CancelCameraButton/>
                    <AddCameraButton />
                </div>
            </form>
        </div>
    )
}