export function ProductCardSkeleton() {
    return (
        <div className="card animate-pulse">
            <div className="aspect-square bg-gray-200" />
            <div className="p-4 space-y-3">
                <div className="h-3 bg-gray-200 rounded w-1/4" />
                <div className="h-4 bg-gray-200 rounded w-3/4" />
                <div className="h-4 bg-gray-200 rounded w-1/2" />
                <div className="flex items-center justify-between mt-4">
                    <div className="h-6 bg-gray-200 rounded w-1/3" />
                    <div className="h-10 w-10 bg-gray-200 rounded-lg" />
                </div>
            </div>
        </div>
    );
}

export function ProductGridSkeleton() {
    return (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {[...Array(8)].map((_, i) => (
                <ProductCardSkeleton key={i} />
            ))}
        </div>
    );
}
