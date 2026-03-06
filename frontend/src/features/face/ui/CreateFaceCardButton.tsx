import {useNavigate} from "react-router-dom";

export const CreateFaceCardButton = () => {

    const navigate = useNavigate();

    return(
        <div
            className="bg-gray-50/50 w-full h-full rounded-3xl border-2 border-dashed border-gray-200 hover:border-blue-400 hover:bg-blue-50/30 transition-all duration-300 group cursor-pointer flex flex-col items-center justify-center min-h-100"
            onClick={() => navigate('/faces/new')}
        >
            {/* 중앙 플러스 아이콘 영역 */}
            <div className="relative">
                {/* 배경 원형 애니메이션 효과 */}
                <div className="absolute inset-0 bg-blue-100 rounded-full scale-0 group-hover:scale-150 opacity-0 group-hover:opacity-20 transition-transform duration-500"></div>

                <div className="relative w-16 h-16 bg-white rounded-2xl shadow-sm border border-gray-100 flex items-center justify-center text-gray-400 group-hover:text-blue-500 group-hover:shadow-md group-hover:-translate-y-1 transition-all duration-300">
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        strokeWidth={2.5}
                        stroke="currentColor"
                        className="w-8 h-8"
                    >
                        <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                    </svg>
                </div>
            </div>

            {/* 하단 텍스트 섹션 */}
            <div className="mt-6 text-center">
                <h3 className="text-lg font-bold text-gray-500 group-hover:text-blue-600 transition-colors">
                    새로운 대상 등록
                </h3>
            </div>
        </div>
    )
}