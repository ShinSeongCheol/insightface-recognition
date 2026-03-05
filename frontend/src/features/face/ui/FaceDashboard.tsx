import {useNavigate} from "react-router-dom";
import {mediaUrl} from "@shared/api/media";
import {useFaces} from "../model/useFaces";

export const FaceDashboard = () => {
    const navigate = useNavigate()

    const {faces, loading} = useFaces();

    if (loading) return <div className="p-20 text-center text-xl">데이터를 가져오는 중... 🍲</div>;


    return (
        <div className="max-w-7xl mx-auto px-4 py-8">

            {/* 대시보드 그리드 레이아웃 */}
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
                {faces.map((face) => (
                    <div key={face.id} className="bg-white rounded-3xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 group">

                        {/* 이미지 섹션 */}
                        <div className="relative aspect-square overflow-hidden bg-gray-100">
                            <img
                                src={mediaUrl(face.image_path)}
                                alt={face.name}
                                className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                                onError={(e) => {
                                    const target = e.currentTarget as HTMLImageElement
                                    target.src = "https://via.placeholder.com/400?text=No+Image";
                                }}
                            />
                            <div className="absolute top-3 right-3 bg-white/80 backdrop-blur-md px-3 py-1 rounded-full text-xs font-bold text-gray-700 shadow-sm">
                                ID: {face.id}
                            </div>
                        </div>

                        {/* 이름 및 정보 섹션 */}
                        <div className="p-6">
                            <h3 className="text-xl font-bold text-gray-800 mb-1">{face.name}</h3>
                            <p className="text-sm text-gray-400">
                                {new Date(face.created_at).toLocaleDateString()} 등록됨
                            </p>

                            <button className="w-full mt-5 py-3 bg-blue-50 text-blue-600 font-bold rounded-2xl hover:bg-blue-600 hover:text-white transition-colors duration-200 hover:cursor-pointer"
                                    onClick={() => navigate(`/faces/${face.id}`)}
                            >
                                상세 정보
                            </button>
                        </div>
                    </div>
                ))}

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
            </div>

            {faces.length === 0 && (
                <div className="text-center py-32 bg-gray-50 rounded-3xl border-2 border-dashed border-gray-200">
                    <p className="text-gray-400 text-lg font-medium">아직 등록된 얼굴이 없습니다.</p>
                </div>
            )}
        </div>
    );
}