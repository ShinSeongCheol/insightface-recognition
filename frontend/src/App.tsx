import {Routes, Route, Link, useLocation} from "react-router-dom";
import { useState } from "react";
import Dashboard from "./pages/Dashboard";
// import FaceDetail from "./pages/FaceDetail";
import RegisterPage from "./pages/RegisterPage";
import FaceDetailPage from "@/pages/FaceDetailPage";
import FacePage from "@/pages/FacePage.tsx";

const navItems = [
    { name: "홈", path: "/" },
    { name: "사용자 관리", path: "/faces" },
];

function NavLinks({pathname, onItemClick,}: {
    pathname: string;
    onItemClick?: () => void;
}) {
    return (
        <nav className="mt-4 px-4 space-y-2">
            {navItems.map((item) => (
                <Link
                    key={item.path}
                    to={item.path}
                    onClick={onItemClick}
                    className={`block px-4 py-2.5 rounded-lg transition-colors ${
                        pathname === item.path
                            ? "bg-blue-50 text-blue-700 font-bold"
                            : "text-gray-600 hover:bg-gray-100"
                    }`}
                >
                    {item.name}
                </Link>
            ))}
        </nav>
    );
}

function App() {
    const location = useLocation();
    const [mobileOpen, setMobileOpen] = useState(false);

    return (
        <div className="min-h-screen bg-gray-50 md:flex">
            {/* 모바일 상단 헤더 */}
            <header className="md:hidden sticky top-0 z-40 bg-white/90 backdrop-blur border-b border-gray-200">
                <div className="flex items-center justify-between px-4 py-3">
                    <button
                        type="button"
                        aria-label="메뉴 열기"
                        onClick={() => setMobileOpen(true)}
                        className="inline-flex items-center justify-center rounded-lg p-2 hover:bg-gray-100"
                    >
                        {/* 햄버거 아이콘 */}
                        <svg width="24" height="24" viewBox="0 0 24 24" className="text-gray-700">
                            <path
                                fill="currentColor"
                                d="M4 6h16v2H4V6Zm0 5h16v2H4v-2Zm0 5h16v2H4v-2Z"
                            />
                        </svg>
                    </button>

                    <span className="text-lg font-black text-blue-600">Face AI 🤖</span>

                    {/* 오른쪽 여백(정렬용) */}
                    <div className="w-10" />
                </div>
            </header>

            {/* 데스크톱 사이드바 */}
            <aside className="hidden md:block md:w-64 bg-white border-r border-gray-200">
                <div className="p-6">
                    <span className="text-xl font-black text-blue-600">Face AI 🤖</span>
                </div>
                <NavLinks pathname={location.pathname}/>
            </aside>

            {/* 모바일 오버레이 + 드로어 */}
            {mobileOpen && (
                <div className="md:hidden fixed inset-0 z-50">
                    {/* 배경 오버레이 */}
                    <div
                        className="absolute inset-0 bg-black/40"
                        onClick={() => setMobileOpen(false)}
                    />

                    {/* 드로어 패널 */}
                    <aside className="absolute left-0 top-0 h-full w-72 bg-white shadow-xl">
                        <div className="flex items-center justify-between p-4 border-b border-gray-200">
                            <span className="text-lg font-black text-blue-600">Face AI 🤖</span>
                            <button
                                type="button"
                                aria-label="메뉴 닫기"
                                onClick={() => setMobileOpen(false)}
                                className="rounded-lg p-2 hover:bg-gray-100"
                            >
                                {/* X 아이콘 */}
                                <svg width="24" height="24" viewBox="0 0 24 24" className="text-gray-700">
                                    <path
                                        fill="currentColor"
                                        d="M18.3 5.71 12 12l6.3 6.29-1.41 1.42L10.59 13.4 4.29 19.71 2.88 18.3 9.17 12 2.88 5.71 4.29 4.29l6.3 6.3 6.29-6.3 1.42 1.42Z"
                                    />
                                </svg>
                            </button>
                        </div>

                        {/* 링크 클릭하면 닫히게 */}
                        <NavLinks pathname={location.pathname} onItemClick={() => setMobileOpen(false)} />
                    </aside>
                </div>
            )}

            {/* 메인 컨텐츠 */}
            <main className="flex-1 p-4 sm:p-6 md:p-10">
                <Routes>
                    <Route path="/" element={<Dashboard />} />

                    <Route path="/faces" element={<FacePage />} />
                    <Route path="/faces/:id" element={<FaceDetailPage />} />
                    <Route path="/faces/new" element={<RegisterPage />} />

                    {/*  출입 기록  */}
                </Routes>
            </main>
        </div>
    );
}

export default App;