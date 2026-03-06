import {FaceCard} from "@/entities/face";
import {CreateFaceCardButton, ViewDetailFaceButton} from "@features/face";
import {useFaces} from "../model/useFaces";

export const FaceWidget = () => {

    const {faces, loading} = useFaces();

    if (loading) return <div className="p-20 text-center text-xl">데이터를 가져오는 중... 🍲</div>;

    return (
        <div className="max-w-7xl mx-auto px-4 py-8">

            {/* 대시보드 그리드 레이아웃 */}
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
                {faces.map((face) => (
                    <FaceCard face={face} action={<ViewDetailFaceButton faceId={face.id}/>}/>
                ))}
                <CreateFaceCardButton/>
            </div>

            {faces.length === 0 && (
                <div className="text-center py-32 bg-gray-50 rounded-3xl border-2 border-dashed border-gray-200">
                    <p className="text-gray-400 text-lg font-medium">아직 등록된 얼굴이 없습니다.</p>
                </div>
            )}
        </div>
    )
}