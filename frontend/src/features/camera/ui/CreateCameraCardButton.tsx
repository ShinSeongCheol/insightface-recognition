import {useNavigate} from "react-router-dom";

export const CreateCameraCardButton = () => {
    const navigate = useNavigate();

    return(
        <div
            className="h-full bg-white rounded-xl overflow-hidden border-2 border-dashed border-gray-300 shadow-xl transition hover:border-blue-400 hover:bg-blue-50/30 group cursor-pointer flex flex-col"
            onClick={() => navigate('/cameras/new')}
        >
            <div className="aspect-video bg-gray-50 flex items-center justify-center border-b border-dashed border-gray-200 group-hover:bg-blue-50 transition-colors">
                <div className="relative">
                    {/* 배경 원형 애니메이션 */}
                    <div className="absolute inset-0 bg-blue-100 rounded-full scale-0 group-hover:scale-150 opacity-0 group-hover:opacity-40 transition-transform duration-500"></div>

                    {/* 플러스 아이콘 */}
                    <div className="relative w-12 h-12 bg-white rounded-xl shadow-sm border border-gray-100 flex items-center justify-center text-gray-400 group-hover:text-blue-500 group-hover:shadow-md group-hover:-translate-y-1 transition-all duration-300">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2.5} stroke="currentColor" className="w-6 h-6">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                        </svg>
                    </div>
                </div>
            </div>

            <div className="p-4 flex flex-col flex-1 justify-center items-center text-center">
                <h3 className="font-semibold text-gray-500 group-hover:text-blue-600 transition-colors">
                    새로운 카메라 등록
                </h3>
                <p className="text-xs text-gray-400 mt-1 opacity-0 group-hover:opacity-100 transition-opacity">
                    클릭하여 장치를 추가하세요
                </p>

                <div className="w-full mt-4 h-7.5 border border-transparent"></div>
            </div>
        </div>
    )
}