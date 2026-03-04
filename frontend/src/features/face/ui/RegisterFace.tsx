import {useRegisterFace} from '../model/useRegisterFace'

export const RegisterFace = () => {

    const {name, preview, isSubmitting, handleFileChange, handleNameChange, handleSubmit} = useRegisterFace();

    return (
        <div className="max-w-2xl mx-auto py-10 px-4">
            <header className="mb-10 text-center">
                <h1 className="text-4xl font-black text-gray-900">새로운 얼굴 등록</h1>
                <p className="text-gray-500 mt-2">이름과 사진을 등록하여 AI가 인식할 수 있게 합니다.</p>
            </header>

            <form onSubmit={handleSubmit} className="bg-white p-8 rounded-[2.5rem] shadow-xl border border-gray-100 space-y-8">
                {/* 사진 업로드 섹션 */}
                <div className="flex flex-col items-center">
                    <div className="relative w-48 h-48 mb-4 group">
                        {preview ? (
                            <img
                                src={preview}
                                alt="Preview"
                                className="w-full h-full object-cover rounded-3xl border-4 border-blue-50"
                            />
                        ) : (
                            <div className="w-full h-full bg-gray-100 rounded-3xl flex flex-col items-center justify-center border-2 border-dashed border-gray-300">
                                <span className="text-4xl mb-2">📸</span>
                                <span className="text-xs text-gray-400">사진을 선택하세요</span>
                            </div>
                        )}
                        <label className="absolute inset-0 cursor-pointer flex items-center justify-center bg-black/40 text-white opacity-0 group-hover:opacity-100 transition-opacity rounded-3xl font-bold">
                            사진 변경
                            <input type="file" className="hidden" accept="image/*" onChange={handleFileChange} />
                        </label>
                    </div>
                </div>

                {/* 이름 입력 섹션 */}
                <div className="space-y-2">
                    <label className="text-sm font-bold text-gray-700 ml-1">사용자 이름</label>
                    <input
                        type="text"
                        placeholder="이름을 입력하세요."
                        className="w-full px-6 py-4 bg-gray-50 border-none rounded-2xl focus:ring-2 focus:ring-blue-500 text-lg font-medium"
                        value={name}
                        onChange={handleNameChange}
                    />
                </div>

                {/* 전송 버튼 */}
                <button
                    type="submit"
                    disabled={isSubmitting}
                    className={`w-full py-5 rounded-2xl font-black text-xl shadow-lg transition-all ${
                        isSubmitting
                            ? 'bg-gray-300 cursor-not-allowed'
                            : 'bg-blue-600 text-white hover:bg-blue-700 active:scale-[0.98] hover:cursor-pointer'
                    }`}
                >
                    {isSubmitting ? "처리 중... 🍲" : "얼굴 데이터 등록하기"}
                </button>

                <p className="text-center text-xs text-gray-400">
                    * 고품질의 정면 사진일수록 인식률이 올라갑니다.
                </p>
            </form>
        </div>
    )
}