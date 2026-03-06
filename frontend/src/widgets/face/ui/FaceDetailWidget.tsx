import {FaceDetailCard} from "@/entities/face";
import {useFaceDetail} from "@/widgets/face/model/useFaceDetail.ts";
import type {Face} from "@/entities/face/api/types.ts";
import {CancelFaceButton, DeleteFaceButton, EditFaceButton, SaveFaceButton} from "@features/face";

export const FaceDetailWidget = () => {
    const { face, isEditing, setIsEditing, newName, setFace, onChangeNewName } = useFaceDetail();

    if (!face) return <div>불러오는 중...</div>;

    return (
        <div className="w-full max-w-5xl mx-auto px-3 sm:px-4 md:px-6 py-3 sm:py-6 md:py-10">
            {face.id ?
                <FaceDetailCard
                    face={face as Face}
                    newName={newName}
                    onChangeNewName={onChangeNewName}
                    isEditing={isEditing}
                    saveButton={<SaveFaceButton faceId={face.id} newName={newName} setIsEditing={setIsEditing} setFace={setFace}/>}
                    cancelButton={<CancelFaceButton setIsEditing={setIsEditing}/>}
                    editButton={<EditFaceButton setIsEditing={setIsEditing}/>}
                    deleteButton={<DeleteFaceButton faceId={face.id}/>}
                />
                : <div>데이터가 없습니다.</div>}
        </div>
    );
}