import {mediaUrl} from "@shared/api/media.ts";
import {useFaceDetail} from "@features/face/model/useFaceDetail.ts";

export const FaceDetail = () => {

    const {face, newName, isEditing, toggleEditing, setNewName, handleUpdate, handleDelete} = useFaceDetail()

    if (!face) return <div className="p-20 text-center">불러오는 중...</div>;

    return(
            <div className="w-full max-w-5xl mx-auto px-3 sm:px-4 md:px-6 py-3 sm:py-6 md:py-10">
                <div className="bg-white rounded-3xl md:rounded-4xl shadow-2xl overflow-hidden flex flex-col md:flex-row border border-gray-100">
                    {/* 이미지 섹션 */}
                    <div className="w-full md:w-1/2 bg-gray-50">
                        <img
                            src={mediaUrl(face?.image_path ?? "")}
                            alt={face?.name ?? "face"}
                            className="w-full h-64 sm:h-80 md:h-full object-cover"
                        />
                    </div>

                    {/* 정보 및 버튼 섹션 */}
                    <div className="w-full md:w-1/2 p-5 sm:p-6 md:p-12 flex flex-col">
                        <div className="flex-1 flex flex-col justify-between items-start">
                            <div className="w-full">
                                <span className="inline-block bg-blue-100 text-blue-600 px-3 py-1 rounded-full text-[11px] sm:text-xs font-bold uppercase">
                                Face ID: {face?.id}
                                </span>

                                {isEditing ? (
                                    <input
                                        type="text"
                                        className="block w-full text-2xl sm:text-3xl md:text-4xl font-black mt-4 sm:mt-6 p-2 border-b-4 border-blue-600 focus:outline-none"
                                        value={newName}
                                        onChange={(e) => setNewName(e.currentTarget.value)}
                                        autoFocus
                                    />
                                ) : (
                                    <h1 className="text-3xl sm:text-4xl md:text-5xl font-black text-gray-900 mt-4 sm:mt-6 wrap-break-word">
                                        {face?.name}
                                    </h1>
                                )}
                            </div>

                            <div className="mt-6 sm:mt-8 space-y-2 text-sm sm:text-base text-gray-500">
                                <p>📅 등록 일자: {face?.created_at ? new Date(face.created_at).toLocaleString() : "-"}</p>
                            </div>
                        </div>

                        {/* 액션 버튼 */}
                        <div className="mt-6 sm:mt-8 md:mt-12 flex flex-col sm:flex-row gap-3 sm:gap-4">
                            {isEditing ? (
                                <>
                                    <button
                                        onClick={handleUpdate}
                                        className="w-full sm:flex-1 bg-blue-600 text-white py-3 sm:py-4 rounded-2xl font-bold shadow-lg hover:bg-blue-700 transition hover:cursor-pointer"
                                    >
                                        저장하기
                                    </button>
                                    <button
                                        onClick={() => toggleEditing(false)}
                                        className="w-full sm:flex-1 bg-gray-100 text-gray-600 py-3 sm:py-4 rounded-2xl font-bold hover:bg-gray-200 transition"
                                    >
                                        취소
                                    </button>
                                </>
                            ) : (
                                <>
                                    <button
                                        onClick={() => toggleEditing(true)}
                                        className="w-full sm:flex-1 bg-blue-600 text-white py-3 sm:py-4 rounded-2xl font-bold shadow-lg hover:bg-blue-500 transition  hover:cursor-pointer"
                                    >
                                        정보 수정
                                    </button>
                                    <button
                                        onClick={handleDelete}
                                        className="w-full sm:flex-1 bg-red-50 text-red-600 py-3 sm:py-4 rounded-2xl font-bold hover:bg-red-100 transition  hover:cursor-pointer"
                                    >
                                        삭제
                                    </button>
                                </>
                            )}
                        </div>
                    </div>
                </div>
        </div>
    )
}